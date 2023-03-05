from password_validation import PasswordPolicy


def is_secure_password(password, common_password_list=''):
    # See https://pypi.org/project/password-validator/

    policy = PasswordPolicy()
    policy = PasswordPolicy(symbols=1, min_length=8, max_length=128, uppercase=1, lowercase=1, numbers=1)
    test = policy.test_password(password, failures_only=True)
    boolean_result = policy.validate(password)
    return [boolean_result, test]


def export_for_html(test_results_list):
    # tests_results_list is refers to the return value of is_secure_password()
    boolean_result = test_results_list[0]
    test_results = test_results_list[1]
    unfulfilled_req_list = []
    if boolean_result != True:
        for unfulfilled_req in test_results:
            # print(unfulfilled_req.name)
            unfulfilled_req_list.append(unfulfilled_req.name)
    return unfulfilled_req_list


def subroutine(password, common_password_list=''):
    text_mapping = {'the minimum number of uppercase characters': "at least one uppercase character",
                    'the minimum number of number characters': "at least one number",
                    'the minimum number of symbol characters': "at least one symbol",
                    'the minimum password length': "in between 8 to 128 characters inclusive",
                    'the minimum number of lowercase characters': "at least one lowercase character"}
    unfulfilled_req_list = export_for_html(is_secure_password(password, common_password_list))
    export_list = []
    for key, value in text_mapping.items():
        if key in unfulfilled_req_list:
            export_list.append(f"✕ {text_mapping[key]}")
        else:
            export_list.append(f"✓ {text_mapping[key]}")

    return export_list


if __name__ == '__main__':
    print(subroutine("j"))
    # print(is_secure_password("jiggerR^2"))
    # print(is_secure_password("password"))
