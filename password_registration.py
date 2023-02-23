from password_validation import PasswordPolicy

def is_secure_password(password, common_password_list=''):
    #See https://pypi.org/project/password-validator/

    policy = PasswordPolicy()
    policy = PasswordPolicy(symbols=1, min_length=8, max_length=128, uppercase=1, lowercase=1, numbers=1)
    test = policy.test_password(password, failures_only=True)
    boolean_result = policy.validate(password)
    return [boolean_result, test]

def export_for_html(test_results_list):
    boolean_result = test_results_list[0]
    test_results = test_results_list[1]
    unfulfilled_req_list = []
    if boolean_result != True:
        for unfulfilled_req in test_results:
            #print(unfulfilled_req.name)
            unfulfilled_req_list.append(unfulfilled_req.name)
    return unfulfilled_req_list

if __name__ == '__main__':
    print(export_for_html(is_secure_password("j")))
    #print(is_secure_password("jiggerR^2"))
    #print(is_secure_password("password"))
