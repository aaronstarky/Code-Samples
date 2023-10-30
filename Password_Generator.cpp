#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
using namespace std;

class PasswordGenerator 
{
public:
    string member_variable = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";

    string generate_password() 
    {
        string password = "";
        srand(time(NULL));
        for (int i = 0; i < 12; i++) 
        {
            int random_index = rand() % member_variable.size();
            password += member_variable[random_index];
        }
        return password;
    }
};
