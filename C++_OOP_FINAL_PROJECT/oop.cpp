#include <iostream>
#include <string>
using namespace std;

// =====================
// STRUCT: Date
// =====================
struct Date {
    int day, month, year;
};

// =====================
// STRUCT: WorkDay
// =====================
struct WorkDay {
    Date* date;
    int hours;
};

// =====================
// CLASS: EmployeeBase
// =====================
class EmployeeBase {
protected:
    string name;
    WorkDay* days;   // Dynamic array of workdays
    int dayCount;

public:
    // Constructor
    EmployeeBase(string n) {
        name = n;
        days = NULL;
        dayCount = 0;
    }

    // Destructor
    virtual ~EmployeeBase() {
        for (int i = 0; i < dayCount; ++i) {
            delete days[i].date;  // Clean up individual date memory
        }
        delete[] days;  // Clean up workday array
    }

    // Adds a new WorkDay, resizes array dynamically
    void addWorkDay(WorkDay newDay) {
        WorkDay* temp = new WorkDay[dayCount + 1];
        for (int i = 0; i < dayCount; ++i) {
            temp[i] = days[i];  // Copy existing days
        }
        temp[dayCount] = newDay;  // Add new day
        delete[] days;
        days = temp;
        dayCount++;
    }

    // Removes a WorkDay at a given index, resizes array
    void removeWorkDay(int index) {
        if (index < 0 || index >= dayCount)
            return;

        delete days[index].date;  // Free memory of date object

        WorkDay* temp = new WorkDay[dayCount - 1];
        for (int i = 0, j = 0; i < dayCount; ++i) {
            if (i != index)
                temp[j++] = days[i];
        }
        delete[] days;
        days = temp;
        dayCount--;
    }

    int getDayCount() const { return dayCount; }

    void showWorkDays() const {
        cout << "Workdays for " << name << ":\n";
        for (int i = 0; i < dayCount; ++i) {
            cout << "  [" << i << "] Date: " 
                 << days[i].date->day << "/" << days[i].date->month << "/" << days[i].date->year
                 << " | Hours: " << days[i].hours << endl;
        }
        if(dayCount == 0) cout << "  No workdays recorded.\n";
    }

    // Pure virtual method for calculating pay
    virtual float calcPay() = 0;

    // Display basic employee info
    virtual void showInfo() {
        cout << "Employee: " << name << endl;
    }
};

// ===========================
// CLASS: HourlyEmployee
// ===========================
class HourlyEmployee : public EmployeeBase {
private:
    float hourlyRate;

public:
    HourlyEmployee(string n, float rate) : EmployeeBase(n) {
        hourlyRate = rate;
    }

    // Calculates pay based on hours with overtime
    float calcPay() override {
        float totalPay = 0;
        for (int i = 0; i < dayCount; ++i) {
            int h = days[i].hours;
            if (h > 8)
                totalPay += 8 * hourlyRate + (h - 8) * hourlyRate * 1.5f;
            else
                totalPay += h * hourlyRate;
        }
        return totalPay;
    }

    void showInfo() override {
        cout << "Hourly Employee: " << name
             << " | Rate: " << hourlyRate << " RWF/hour" << endl;
    }
};

// ============================
// CLASS: SalariedEmployee
// ============================
class SalariedEmployee : public EmployeeBase {
private:
    float monthlySalary;

public:
    SalariedEmployee(string n, float salary) : EmployeeBase(n) {
        monthlySalary = salary;
    }

    // Returns fixed salary
    float calcPay() override {
        return monthlySalary;
    }

    void showInfo() override {
        cout << "Salaried Employee: " << name
             << " | Monthly Salary: " << monthlySalary << " RWF" << endl;
    }
};

// =====================
// MAIN FUNCTION
// =====================
int main() {
    cout << "=================================\n";
    cout << "  EMPLOYEE PAYROLL SYSTEM  \n";
    cout << "=================================\n\n";

    int num;
    cout << "Enter number of employees: ";
    cin >> num;
    cin.ignore();  // Clear newline character from input

    EmployeeBase** staff = new EmployeeBase*[num];  // Array of base class pointers

    for (int i = 0; i < num; ++i) {
        cout << "\n--- EMPLOYEE #" << (i + 1) << " DATA ENTRY ---\n";

        string name, type;
        cout << "Enter name of employee: ";
        getline(cin, name);

        cout << "Enter type (hourly/salaried): ";
        getline(cin, type);

        if (type == "hourly") {
            float rate;
            cout << "Enter hourly rate (RWF): ";
            cin >> rate;
            cin.ignore();
            staff[i] = new HourlyEmployee(name, rate);
        } else if (type == "salaried") {
            float salary;
            cout << "Enter monthly salary (RWF): ";
            cin >> salary;
            cin.ignore();
            staff[i] = new SalariedEmployee(name, salary);
        } else {
            cout << "Invalid type. Skipping employee.\n";
            i--;
            continue;
        }

        int numDays;
        cout << "Enter number of workdays for " << name << ": ";
        cin >> numDays;
        cin.ignore();

        cout << "\n-- WORKDAY ENTRIES --\n";
        for (int d = 0; d < numDays; ++d) {
            int dd, mm, yy, hrs;
            cout << "  WorkDay " << (d + 1) << " - Enter date (dd mm yyyy): ";
            cin >> dd >> mm >> yy;
            cout << "  Enter hours worked: ";
            cin >> hrs;
            cin.ignore();

            WorkDay w;
            w.date = new Date;
            w.date->day = dd;
            w.date->month = mm;
            w.date->year = yy;
            w.hours = hrs;

            staff[i]->addWorkDay(w);  // Add to employee record
        }

        // --- Interactive Add/Remove WorkDay menu ---
        char choice;
        do {
            cout << "\nCurrent workdays for " << name << ":\n";
            staff[i]->showWorkDays();

            cout << "\nOptions for " << name << ":\n";
            cout << "  a - Add a workday\n";
            cout << "  r - Remove a workday\n";
            cout << "  q - Quit editing workdays\n";
            cout << "Enter choice (a/r/q): ";
            cin >> choice;
            cin.ignore();

            if (choice == 'a') {
                int dd, mm, yy, hrs;
                cout << "Enter date to add (dd mm yyyy): ";
                cin >> dd >> mm >> yy;
                cout << "Enter hours worked: ";
                cin >> hrs;
                cin.ignore();

                WorkDay w;
                w.date = new Date;
                w.date->day = dd;
                w.date->month = mm;
                w.date->year = yy;
                w.hours = hrs;

                staff[i]->addWorkDay(w);
                cout << "Workday added.\n";

            } else if (choice == 'r') {
                if (staff[i]->getDayCount() == 0) {
                    cout << "No workdays to remove.\n";
                    continue;
                }
                int idx;
                cout << "Enter index of workday to remove: ";
                cin >> idx;
                cin.ignore();

                if (idx >= 0 && idx < staff[i]->getDayCount()) {
                    staff[i]->removeWorkDay(idx);
                    cout << "Workday removed.\n";
                } else {
                    cout << "Invalid index.\n";
                }
            } else if (choice != 'q') {
                cout << "Invalid choice. Please enter a, r, or q.\n";
            }
        } while (choice != 'q');
    }

    // Generate Payroll Report
    cout << "\n\n=================================\n";
    cout << "         PAYROLL REPORT         \n";
    cout << "=================================\n";
    for (int i = 0; i < num; ++i) {
        cout << "\n--- EMPLOYEE #" << (i + 1) << " ---\n";
        staff[i]->showInfo();
        cout << "Total Pay: " << staff[i]->calcPay() << " RWF" << endl;
    }

    // Cleanup memory
    for (int i = 0; i < num; ++i)
        delete staff[i];
    delete[] staff;

    cout << "\n=================================\n";
    cout << "  END OF PAYROLL PROCESSING  \n";
    cout << "=================================\n";

    return 0;
}

