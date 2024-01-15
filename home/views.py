from django.shortcuts import redirect, render
from home.models import *
from home.views import *
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,"index.html")

# EMPLOYEE SECTION
def employee_home(request):
    if request.method=='POST':
        data=request.POST
        employee_id=data.get('employee_id')
        employee_name=data.get('employee_name')

        if (Employee.objects.filter(Employee_id=employee_id)):
            messages.error(request, "Employee Id already Exists ! ")
            return redirect("/employee/")

        Employee.objects.create(Employee_id = employee_id,Employee_name = employee_name)
        messages.success(request, "Record Inserted Successfully !")
        return redirect("/employee/")
    

    Employee_all=Employee.objects.all()
    context={
        'Employee_all' : Employee_all,
        'Title': "Employee | Home",
        'back_url' : "/ " 
    }
    return render(request, "employee_home.html",context)

def employee_update(request,id):

    emp=Employee.objects.get(Employee_id=id)
    if request.method=='POST':
        data=request.POST
        employee_id=data.get('employee_id')
        employee_name=data.get('employee_name')
        
        if(employee_id!=id): # employee id is changed
            if (Employee.objects.filter(Employee_id = employee_id)):    # changed employee id is  already present
                messages.error(request, "This Employee Id is already assigned to a employee ! ")
                return redirect("/employee-update/{0}".format(id))
            else:
                Employee.objects.create(Employee_id = employee_id,Employee_name = employee_name)
                emp.delete()
        else:
            emp.Employee_name = employee_name
            emp.save()
        
        return redirect("/employee/")
    
    
    context={
        'Employee':emp,
        'Title': "Employee | Update",
        'back_url' : "/employee/"
    }
    return render(request, "employee_update.html",context)

def employee_delete(request,id):
    emp=Employee.objects.get(Employee_id=id)
    emp.delete()
    return redirect("/employee/")
    

# DEPARTMENT SECTION

def department_home(request):
    if request.method=='POST':
        data=request.POST
        department_id=data.get('department_id')
        department_name=data.get('department_name')
        department_manager_id=data.get('department_manager_id')

        if Departments.objects.filter(Department_id=department_id):
            messages.error(request, "This Department Id is already assigned to a Department ! ")
            return redirect("/department/")
         
        if Employee.objects.filter(Employee_id=department_manager_id):
            
            emp=Employee.objects.get(Employee_id=department_manager_id)
            if Departments.objects.filter(Department_manager=emp):
                messages.error(request, "This Employee is already assigned to a Department as Manager ! ")
                return redirect("/department/")

            manager_obj=Employee.objects.get(Employee_id=department_manager_id)
            Departments.objects.create(Department_id = department_id,Department_name = department_name,Department_manager = manager_obj)
        
        else:
            messages.error(request, "No Employee exists with this Employee Id ! ")
            return redirect("/department/")
            
        messages.success(request, "Record Inserted Successfully !")
        return redirect("/department/")
    

    Department_all=Departments.objects.all()
    context={
        'Department_all' : Department_all,
        'Title': "Department | Home",
        'back_url' : "/ "
    }

    return render(request,"department_home.html",context)

def department_update(request,id):
    
    dept=Departments.objects.get(Department_id=id)
    manager_obj=dept.Department_manager
    
    if request.method=='POST':

        data=request.POST
        department_id=data.get('department_id')
        department_name=data.get('department_name')
        department_manager_id=int(data.get('department_manager_id'))


        if(id!=department_id):
            if Departments.objects.filter(Department_id=department_id):
                messages.error(request, "This Department Id is already assigned to a Department ! ")
                return redirect("/department-update/{}".format(id))
            
        
        if(manager_obj.Employee_id!= department_manager_id):
            print("hii")
            if not Employee.objects.filter(Employee_id=department_manager_id): # manager is not an employee
                messages.error(request, "This Employee Id does not exist ! ")
                return redirect("/department-update/{}".format(id))
                
            emp=Employee.objects.get(Employee_id=department_manager_id)
            if Departments.objects.filter(Department_manager=emp):  # already a manager
                messages.error(request, "This Employee is already assigned to another Department as Manager ! ")
                return redirect("/department-update/{}".format(id))
                    
            manager_obj=Employee.objects.get(Employee_id=department_manager_id)


        dept.delete()
        Departments.objects.create(Department_id = department_id,Department_name = department_name,Department_manager = manager_obj)
        messages.success(request, "Record Updated Successfully !")                 
        return redirect("/department-update/{}".format(department_id))
    
    
    context={
        'Dept':dept,
        'Title': "Department | Update",
        'back_url' : "/department/"
    }
    return render(request,"department_update.html",context)

def department_delete(request,id):
    dept=Departments.objects.get(Department_id=id)
    dept.delete()
    return redirect("/department/")