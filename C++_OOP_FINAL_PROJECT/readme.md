Payroll System with Overtime – Object-Oriented Programming Assignment


Introduction
This project is focused on building a Payroll System that manages employee working hours, computes payments including overtime, and utilizes object-oriented programming (OOP) concepts in C++. It highlights the application of inheritance, polymorphism, and dynamic memory management to develop a flexible and scalable solution.
WorkDay Structure
The foundation of this system begins with defining a struct named WorkDay, which contains:
- A pointer to a Date structure.
- An integer value representing the number of hours worked.

Each employee will have a dynamically allocated array of WorkDay entries. This array will store the employee's daily work logs and must be resizable to allow for adding or removing workdays.
Employee Class Hierarchy
At the core of the system is an abstract class EmployeeBase, which includes the following:
- Common attributes like employee name.
- A virtual function calcPay() marked as = 0, making the class abstract.
- A pointer to a dynamically allocated array of WorkDay.
- Functions for managing work logs (adding and removing days).

This base class is then extended by two derived classes:
1. HourlyEmployee – Calculates pay based on the number of hours worked, with overtime paid at 1.5× the regular rate for hours exceeding 8 hours per day.
2. SalariedEmployee – Receives a fixed monthly salary regardless of the number of hours worked.

This structure demonstrates inheritance and polymorphism, allowing different employee types to implement their own version of the calcPay() function.
Dynamic Employee Management
Employees are stored using a dynamic array of base class pointers:
EmployeeBase** staff;

This approach makes it possible to handle different employee types uniformly. When calling staff[i]->calcPay(), the correct method is automatically dispatched based on the actual object type (Hourly or Salaried), showing the power of runtime polymorphism in C++.
Pointer Arithmetic and Overtime Calculations
For HourlyEmployee, the system uses pointer arithmetic to loop through the array of WorkDay entries, summing the number of hours worked each day. If any day's hours exceed 8, those extra hours are calculated at the overtime rate of 1.5× the normal pay.

This precise handling of hours ensures accurate payroll calculations for hourly employees.
Dynamic Work Log Management
To allow flexible management of daily work logs, the system implements two core functions:

- addWorkDay(WorkDay): Adds a new workday to the employee's record, resizing the array and copying over existing data.
- removeWorkDay(int index): Removes a workday at the given index, again resizing the array to maintain accurate logs without memory leaks.

These functions reinforce the importance of dynamic memory allocation and deallocation, a crucial aspect of C++ programming.

 HERE ARE DETAILED CODE WITH EVERY COMMENT

 
 #include <iostream> : Includes the iostream library, essential for input and output operations like 'cout' (for printing) and 'cin' (for reading).
#include <string>  : Includes the string library, which provides the 'string' class for working with sequences of characters.
using namespace std; : This line brings the 'std' namespace into scope, so you don't have to type 'std::' before standard library elements like 'cout', 'cin', and 'string'.
STRUCT: Date
struct Date { : Defines a structure named 'Date'. Structures are user-defined data types that can group related data members.
 int day, month, year; :Declares three integer members: 'day', 'month', and 'year'. These will store the components of a date.
};
 STRUCT: WorkDay
struct WorkDay { :Defines a structure named 'WorkDay'.
 Date* date; : Declares a pointer to a 'Date' object. This means a 'WorkDay' will hold a memory address where a 'Date' object is stored. Using a pointer allows dynamic allocation of Date objects.
 int hours; :Declares an integer member named 'hours' to store the number of hours worked on a particular day.
};
CLASS: EmployeeBase
class EmployeeBase { : Defines a base class named 'EmployeeBase'. This class serves as a blueprint for all types of employees.
protected:  : The 'protected' access specifier means these members can be accessed by the class itself and any classes derived from it.
 string name;  :A string to store the employee's name.
 WorkDay* days; : A pointer to a 'WorkDay' object. This will be used as a dynamic array to store multiple 'WorkDay' records for the employee.
 int dayCount;    : An integer to keep track of the current number of workdays stored in the 'days' array.

public: : The 'public' access specifier means these members can be accessed from outside the class.
 :Constructor
 EmployeeBase(string n) { : This is the constructor for the 'EmployeeBase' class. It's called when an object of this class (or a derived class) is created. It takes a string 'n' as the employee's name.
    name = n;   :Initializes the 'name' member with the provided string 'n'.
    days = NULL;     :Initializes the 'days' pointer to 'NULL'. This signifies that the dynamic array of workdays is empty initially.
    dayCount = 0;   :Initializes 'dayCount' to 0, as there are no workdays recorded yet.
    }
    : Destructor
    virtual ~EmployeeBase() { : This is the virtual destructor for 'EmployeeBase'. It's called when an object is destroyed. The 'virtual' keyword is crucial for polymorphism; it ensures the correct destructor (of the most derived class) is called when deleting objects via a base class pointer.
      for (int i = 0; i < dayCount; ++i) { :Loops through each 'WorkDay' entry in the 'days' array.
      delete days[i].date; : Deallocates the memory pointed to by the 'date' member of each 'WorkDay'. This is important because 'w.date = new Date;' allocates memory dynamically.
        }
     delete[] days; : Deallocates the memory for the entire 'days' dynamic array. This cleans up the memory allocated for the array itself.
    }
 : Adds a new WorkDay, resizes array dynamically
   void addWorkDay(WorkDay newDay) { : This method adds a new 'WorkDay' to the employee's record. It handles dynamic resizing of the 'days' array.
    WorkDay* temp = new WorkDay[dayCount + 1]; : Creates a new dynamic array named 'temp' that is one element larger than the current 'days' array.
    for (int i = 0; i < dayCount; ++i) { :Loops through all the existing workdays.
    temp[i] = days[i]; : Copies each existing 'WorkDay' from the old 'days' array to the new 'temp' array.
        }
   temp[dayCount] = newDay; : Adds the 'newDay' (the workday being added) to the last position of the 'temp' array.
     delete[] days;    :Deallocates the memory occupied by the old 'days' array.
       days = temp: Points the 'days' pointer to the new 'temp' array, effectively replacing the old array with the larger one.
       dayCount++;   :Increments 'dayCount' to reflect the addition of the new workday.
    }
 :Removes a WorkDay at a given index, resizes array
    void removeWorkDay(int index) { : This method removes a 'WorkDay' at a specified 'index' from the employee's record, also resizing the array dynamically.
     if (index < 0 || index >= dayCount) : Checks if the provided 'index' is valid (within the bounds of the array).
     return; : If the index is out of bounds, the function simply returns without doing anything.

        delete days[index].date;: Before removing the 'WorkDay' entry, it deallocates the 'Date' object associated with that 'WorkDay' to prevent memory leaks.

        WorkDay* temp = new WorkDay[dayCount - 1]; : Creates a new dynamic array named 'temp' that is one element smaller than the current 'days' array.
        for (int i = 0, j = 0; i < dayCount; ++i) { : Loops through the existing workdays. 'j' is used as an index for the 'temp' array.
        if (i != index) : If the current index 'i' is NOT the index of the workday to be removed...
        temp[j++] = days[i]; : ...then copy the 'WorkDay' from the old 'days' array to the 'temp' array and increment 'j'.
        }
        delete[] days;  : Deallocates the memory occupied by the old 'days' array.
        days = temp;  : Points the 'days' pointer to the new 'temp' array, effectively replacing the old array with the smaller one.
        dayCount--;   : Decrements 'dayCount' to reflect the removal of a workday.
    }

    int getDayCount() const { return dayCount; } : A 'const' method that returns the current number of workdays. 'const' means this method doesn't modify the object's state.

    void showWorkDays() const { : A 'const' method that displays all the recorded workdays for the employee.
     cout << "Workdays for " << name << ":\n"; : Prints a header indicating whose workdays are being displayed.
      for (int i = 0; i < dayCount; ++i) { : Loops through each 'WorkDay' in the 'days' array.
     cout << "  [" << i << "] Date: " : Prints the index of the workday.
     << days[i].date->day << "/" << days[i].date->month << "/" << days[i].date->year :Accesses the 'day', 'month', and 'year' members of the 'Date' object pointed to by 'days[i].date' and prints the date in DD/MM/YYYY format.
     << " | Hours: " << days[i].hours << endl;: Prints the hours worked for that day.
        }
        if (dayCount == 0)
         cout << "  No workdays recorded.\n";: If there are no workdays, a message is displayed.
    }
: Pure virtual method for calculating pay
    virtual float calcPay() = 0; :This is a pure virtual method. The '= 0' makes 'EmployeeBase' an abstract class, meaning you cannot create objects directly from 'EmployeeBase'. Any concrete class inheriting from 'EmployeeBase' MUST provide its own implementation for 'calcPay()'. This ensures that every employee type knows how to calculate its pay.

    : Display basic employee info
    virtual void showInfo() { : A virtual method to display basic employee information. 'virtual' allows derived classes to override this method.
    cout << "Employee: " << name << endl; : Prints the general "Employee:" prefix and the employee's name.
    }
};
CLASS: HourlyEmployee
class HourlyEmployee : public EmployeeBase { :Defines a class 'HourlyEmployee' that inherits publicly from 'EmployeeBase'. This means it gets all the public and protected members of 'EmployeeBase'.
private:    :The 'private' access specifier means this member can only be accessed from within the 'HourlyEmployee' class itself.
  float hourlyRate; : A float to store the hourly rate for this type of employee.
public: : Public members of 'HourlyEmployee'.
 HourlyEmployee(string n, float rate) : EmployeeBase(n) { :Constructor for 'HourlyEmployee'. It uses an initializer list ': EmployeeBase(n)' to call the constructor of the base class 'EmployeeBase' with the employee's name.
   hourlyRate = rate; : Initializes the 'hourlyRate' member with the provided 'rate'.
    }
   : Calculates pay based on hours with overtime
   float calcPay() override { : This method overrides the pure virtual 'calcPay()' method from 'EmployeeBase'. The 'override' keyword is a good practice to ensure you are indeed overriding a base class method.
    float totalPay = 0;   :Initializes a float variable to store the total calculated pay.
    for (int i = 0; i < dayCount; ++i) { : Loops through each workday recorded for this employee.
    int h = days[i].hours; : Gets the hours worked for the current workday.
    if (h > 8)  :Checks if the hours worked exceed 8 (indicating overtime).
   totalPay += 8 * hourlyRate + (h - 8) * hourlyRate * 1.5f; :Calculates pay: 8 hours at normal rate + (hours over 8) at 1.5 times the hourly rate.
            else
   totalPay += h * hourlyRate; : If no overtime, calculates pay as hours worked multiplied by the hourly rate.
        }
     return totalPay; : Returns the total calculated pay.
    }

    void showInfo() override { :This method overrides the 'showInfo()' method from 'EmployeeBase' to provide more specific information for an hourly employee.
    cout << "Hourly Employee: " << name  :Prints "Hourly Employee:" and the employee's name.
    << " | Rate: " << hourlyRate << " RWF/hour" << endl; :Prints the hourly rate, indicating the currency (RWF).
    }
};
 CLASS: SalariedEmployee
class SalariedEmployee : public EmployeeBase { :Defines a class 'SalariedEmployee' that also inherits publicly from 'EmployeeBase'.
private:   :Private members of 'SalariedEmployee'.
float monthlySalary; :A float to store the fixed monthly salary for this type of employee.
public: : Public members of 'SalariedEmployee'.
SalariedEmployee(string n, float salary) : EmployeeBase(n) { :Constructor for 'SalariedEmployee'. Calls the base class constructor with the employee's name.
 monthlySalary = salary; : Initializes the 'monthlySalary' member with the provided 'salary'.
    }
:Returns fixed salary
 float calcPay() override { : This method overrides the pure virtual 'calcPay()' method for salaried employees.
 return monthlySalary; : For a salaried employee, the pay is simply their fixed monthly salary, regardless of hours worked.
    }
void showInfo() override { :This method overrides 'showInfo()' to provide specific information for a salaried employee.
 cout << "Salaried Employee: " << name   :Prints "Salaried Employee:" and the employee's name.
  << " | Monthly Salary: " << monthlySalary << " RWF" << endl; : Prints the monthly salary, indicating the currency.
    }
};
MAIN FUNCTION
int main() { :The entry point of the program. Execution begins here.
    cout << "=================================\n"; :Prints a decorative line.
    cout << "  EMPLOYEE PAYROLL SYSTEM  \n";  : Prints the title of the system.
    cout << "=================================\n\n"; : Prints another decorative line and some newlines for formatting.
    int num; : Declares an integer variable to store the number of employees the user wants to enter.
    cout << "Enter number of employees: "; : Prompts the user to input the number of employees.
    cin >> num; :Reads the integer input from the user and stores it in 'num'.
    cin.ignore(); : This is crucial! 'cin >> num' reads the number but leaves the newline character ('\n') in the input buffer. 'cin.ignore()' discards this newline, preventing it from being read by subsequent 'getline()' calls.

    EmployeeBase** staff = new EmployeeBase*[num]; : Creates a dynamic array of 'EmployeeBase' pointers. This array will hold pointers to objects of 'HourlyEmployee' or 'SalariedEmployee' (polymorphism).

    for (int i = 0; i < num; ++i) { : A loop that iterates 'num' times, once for each employee to be entered.
     cout << "\n--- EMPLOYEE #" << (i + 1) << " DATA ENTRY ---\n"; : Prints a header for the current employee's data entry.

        string name, type; :Declares string variables for the employee's name and type.
        cout << "Enter name of employee: "; : Prompts the user to enter the employee's name.
        getline(cin, name);    :Reads the entire line of input for the name (important for names with spaces).
        cout << "Enter type (hourly/salaried): "; : Prompts the user to enter the employee's type.
        getline(cin, type);    :Reads the entire line for the type.
        if (type == "hourly") { :Checks if the entered type is "hourly".
            float rate;   :Declares a float variable for the hourly rate.
            cout << "Enter hourly rate (RWF): "; :Prompts for the hourly rate.
            cin >> rate;   :Reads the hourly rate.
            cin.ignore();    :Clears the newline character from the input buffer.
            staff[i] = new HourlyEmployee(name, rate); :Dynamically creates a new 'HourlyEmployee' object using 'name' and 'rate', and stores its pointer in the 'staff' array at index 'i'.
        } else if (type == "salaried") { : Checks if the entered type is "salaried".
            float salary; :Declares a float variable for the monthly salary.
            cout << "Enter monthly salary (RWF): "; : Prompts for the monthly salary.
            cin >> salary;   :Reads the monthly salary.
            cin.ignore(); :Clears the newline character.
            staff[i] = new SalariedEmployee(name, salary); : Dynamically creates a new 'SalariedEmployee' object and stores its pointer.
        } else {
            cout << "Invalid type. Skipping employee.\n"; :Informs the user if an invalid type was entered.
            i--;        : Decrements 'i'. This makes the loop re-execute for the same index, allowing the user to re-enter data for this employee.
            continue;    :Jumps to the beginning of the 'for' loop for the next iteration (or re-try).
        }

        int numDays; :Declares an integer to store the number of workdays for the current employee.
        cout << "Enter number of workdays for " << name << ": "; :Prompts for the number of workdays.
        cin >> numDays; :Reads the number of workdays.
        cin.ignore(); :Clears the newline character.
        cout << "\n-- WORKDAY ENTRIES --\n"; : Prints a header for workday entries.
        for (int d = 0; d < numDays; ++d) {  :A loop to get details for each workday.
            int dd, mm, yy, hrs;  :Declares integers for day, month, year, and hours.
            cout << "  WorkDay " << (d + 1) << " - Enter date (dd mm yyyy): ";: Prompts for the date.
            cin >> dd >> mm >> yy;  :Reads day, month, and year.
            cout << "  Enter hours worked: ";  :Prompts for hours worked.
            cin >> hrs;  :Reads hours worked.
            cin.ignore();    :Clears the newline character.

            WorkDay w;  : Creates a 'WorkDay' struct object.
            w.date = new Date; : Dynamically allocates a new 'Date' object and assigns its memory address to the 'date' pointer within the 'WorkDay' struct.
            w.date->day = dd; : Sets the 'day' member of the newly created 'Date' object.
            w.date->month = mm; :Sets the 'month'.
            w.date->year = yy; : Sets the 'year'.
            w.hours = hrs; : Sets the 'hours' member of the 'WorkDay' struct.

            staff[i]->addWorkDay(w); : Calls the 'addWorkDay' method on the current employee object (pointed to by 'staff[i]') to add the newly created workday.
        }
        : --- Interactive Add/Remove WorkDay menu ---
        char choice; :Declares a character variable to store the user's menu choice.
        do {     :Starts a 'do-while' loop, which ensures the menu is displayed at least once.
       cout << "\nCurrent workdays for " << name << ":\n"; :Shows the current workdays for the employee.
        staff[i]->showWorkDays();  :Calls the 'showWorkDays' method to display the list.

            cout << "\nOptions for " << name << ":\n"; :Presents the interactive options.
            cout << "  a - Add a workday\n";         : Option to add.
            cout << "  r - Remove a workday\n";     : Option to remove.
            cout << "  q - Quit editing workdays\n"; : Option to quit.
            cout << "Enter choice (a/r/q): ";   :Prompts for the user's choice.
            cin >> choice;   :Reads the character choice.
            cin.ignore();     :Clears the newline character.
            if (choice == 'a') { : If the user chose 'a' (add).
                int dd, mm, yy, hrs; : Declares variables for the new workday details.
                cout << "Enter date to add (dd mm yyyy): "; :Prompts for the date.
                cin >> dd >> mm >> yy; :Reads the date components.
                cout << "Enter hours worked: ";  :Prompts for hours.
                cin >> hrs;    :Reads hours.
                cin.ignore();    :Clears the newline.

                WorkDay w;   :Creates a new 'WorkDay' struct.
                w.date = new Date; : Dynamically allocates a 'Date' object.
                w.date->day = dd;  : Sets day.
                w.date->month = mm; :Sets month.
                w.date->year = yy;  :Sets year.
                w.hours = hrs;  : Sets hours.
                staff[i]->addWorkDay(w); : Adds the new workday to the employee's record.
                cout << "Workday added.\n"; : Confirms the addition.
            } else if (choice == 'r') { :If the user chose 'r' (remove).
                if (staff[i]->getDayCount() == 0) { :Checks if there are any workdays to remove.
                    cout << "No workdays to remove.\n"; : Informs the user if the list is empty.
                    continue; : Skips the rest of this iteration and goes back to display the menu.
                }
                int idx; :Declares an integer for the index of the workday to remove.
                cout << "Enter index of workday to remove: "; :Prompts for the index.
                cin >> idx; :Reads the index.
                cin.ignore(); :Clears the newline.
                if (idx >= 0 && idx < staff[i]->getDayCount()) { : Validates the entered index.
                    staff[i]->removeWorkDay(idx); :Calls 'removeWorkDay' to remove the workday.
                    cout << "Workday removed.\n";   :Confirms the removal.
                } else {
                    cout << "Invalid index.\n"; : Informs of an invalid index.
                }
            } else if (choice != 'q') { : If the choice is not 'a', 'r', or 'q'.
                cout << "Invalid choice. Please enter a, r, or q.\n"; :Informs of an invalid menu choice.
            }
        } while (choice != 'q'); :The loop continues as long as the user's choice is not 'q' (quit).
    }
     Generate Payroll Report
    cout << "\n\n=================================\n"; : Prints decorative lines.
    cout << "           PAYROLL REPORT          \n"; : Prints the title of the payroll report.
    cout << "=================================\n";
    for (int i = 0; i < num; ++i) { /:Loop through all the employees to generate their payroll.
        cout << "\n--- EMPLOYEE #" << (i + 1) << " ---\n"; : Prints a header for each employee in the report.
        staff[i]->showInfo(); : Calls the 'showInfo()' method polymorphically (it will call the correct 'showInfo' for 'HourlyEmployee' or 'SalariedEmployee').
        cout << "Total Pay: " << staff[i]->calcPay() << " RWF" << endl; :Calls the 'calcPay()' method polymorphically to get and print the total pay.
    }
    Cleanup memory
    for (int i = 0; i < num; ++i) : Loop through the array of employee pointers.
        delete staff[i];  : Calls the destructor for each 'EmployeeBase' pointer. Due to virtual destructors, this will correctly call the destructor of the actual derived class ('HourlyEmployee' or 'SalariedEmployee'), which in turn calls the base class destructor, ensuring all dynamically allocated memory within the objects is freed.
    delete[] staff;  :Deallocates the memory for the array of 'EmployeeBase' pointers itself.

    cout << "\n=================================\n"; :Prints decorative lines.
    cout << "  END OF PAYROLL PROCESSING  \n";  :Prints a message indicating the end of the program.
    cout << "=================================\n";

    return 0; : Returns 0, indicating that the program executed successfully.
}

![1 text](https://github.com/user-attachments/assets/0caf25ee-0c9f-43d1-9c5e-eae314b8c211)

![2 text](https://github.com/user-attachments/assets/992d93a0-7d02-48bb-85cc-d1e2c4dcd62a)
![3 text](https://github.com/user-attachments/assets/84684cd2-f972-4a5c-9ee8-2480c5973b48)
![4 text](https://github.com/user-attachments/assets/15afb862-846a-4715-ac5f-adef101010da)
![5 text](https://github.com/user-attachments/assets/edfe197f-1ded-42a0-80ca-a645a6922196)
![6 text](https://github.com/user-attachments/assets/72f76d98-ef1a-45fc-b05c-4b5a90bdc146)

Conclusion
This payroll system project is a practical and hands-on application of object-oriented principles in C++. By implementing dynamic memory management, inheritance, and polymorphism, it reflects real-world payroll pr
ocessing requirements. The use of structures, base and derived classes, virtual functions, and pointer manipulation all contribute to a deeper understanding of managing complex systems in C++.

