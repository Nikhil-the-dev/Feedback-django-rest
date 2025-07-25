from django.shortcuts import render,redirect
import requests
from django.contrib import messages
from rest_framework import status
from django.contrib.auth.hashers import check_password

def home(request):
    return render(request,'feedbackapp/home.html')

def admin_register(request):
    if request.method == 'POST':
        admin_register_data = {'email':request.POST.get('adminemail'),'fullname':request.POST.get('adminfullname'),
                               'adminid':request.POST.get('adminusername'),'password':request.POST.get('adminpassword')}
        reg_response = requests.post('http://127.0.0.1:8000/Ad',json=admin_register_data)
        if reg_response.status_code == 201:
            messages.success(request, 'Admin Registerd Successfully')
            return redirect('/admin_login')
        else:
            messages.error(request, 'Admin Registration Failed')
            return redirect('/admin_register')
    return render(request,'feedbackapp/admin_register.html') 

def admin_login(request):
    if request.method == 'POST':
        admin_email = request.POST.get('adminemail')
        admin_password = request.POST.get('adminpassword')
        # Without email and password submittion error
        if not admin_email or not admin_password:
            messages.error(request,'Login Credentials required')
            return redirect('/admin_login')
        data = {'email':admin_email}
        admin_data = requests.get('http://127.0.0.1:8000/Ad',params=data)
        admin_data_response = admin_data.json()
        print(admin_data_response)
        admin = None
        for a in admin_data_response:
            if a['email'] == admin_email:
                if admin_password == a['password']:
                    admin = a
                    break
        if admin:
            request.session['admin_id'] = admin['id']
            request.session['admin_username'] = admin['adminid']
            request.session['admin_fullname'] = admin['fullname']
            request.session['admin_email'] = admin['email']
            messages.success(request,"Login Successfull")
            return redirect('/admin_choice')
        else:
            messages.error(request, 'Invalid Email And Password')
            return redirect('/admin_login')
    return render(request,'feedbackapp/admin_login.html')   

# def admin_login(request):
#     if request.method == "POST":
#         username = request.POST.get('adminemail')
#         password = request.POST.get('adminpassword')
#         if not username and not password:
#             return render(request, 'feedbackapp/admin_login.html',{'error':'Username and Password are requerid'})
#         response = requests.post('http://127.0.0.1:8000/login', json={'username': username, 'password': password})
        
#         if response.ok:  # Check if status code is 200-299
#             # Handle successful login (e.g., store tokens, user info)
#             return render(request, 'feedbackapp/feedback.html', {'data': response.json()})  # Redirect to a success page
#         else:
#             # Handle login failure
#             return render(request, 'feedbackapp/admin_login.html', {'error': response.json()})   
#     return render(request, 'feedbackapp/admin_login.html')

def admin_choice(request):
    admin_id = request.session.get('admin_id')
    admin_username = request.session.get('admin_username')
    admin_email = request.session.get('admin_email')
    if not admin_username or not admin_email:
        return redirect('/admin_login')
    return render(request,'feedbackapp/admin_choice.html',{'admin_username':admin_username})

def admin_view_all_records(request):
    admin_id = request.session.get('admin_id')
    admin_username = request.session.get('admin_username')
    admin_email = request.session.get('admin_email')
    if not admin_username or not admin_email:
        return redirect('/admin_login')
    feed_data_response = requests.get('http://127.0.0.1:8000/feedback')
    if feed_data_response.status_code == 200:
        view_feed_data = feed_data_response.json()
    else:
        view_feed_data = None
    return render(request,'feedbackapp/admin_view_all_records.html',{'view_feed_data':view_feed_data})

def admin_view_all_reply(request):
    admin_id = request.session.get('admin_id')
    admin_username = request.session.get('admin_username')
    admin_email = request.session.get('admin_email')
    if not admin_username or not admin_email:
        return redirect('/admin_login')
    reply_data = requests.get('http://127.0.0.1:8000/reply')
    if reply_data.status_code == 200:
        view_reply_data = reply_data.json()
    else:
        view_reply_data = None
    return render(request,'feedbackapp/admin_view_all_reply.html',{'view_reply_data':view_reply_data})

def admin_view_manager_detail(request):
    admin_username = request.session.get('admin_username')
    admin_email = request.session.get('admin_email')
    if not admin_username or not admin_email:
        return redirect('/admin_login')
    manager_detail = requests.get('http://127.0.0.1:8000/managers')
    if manager_detail.status_code == 200:
        manager_server_response = manager_detail.json()
    else:
        manager_server_response = 'Data Not Fatched Successfully'
    return render(request,'feedbackapp/admin_view_manager_detail.html',{'manager_Details': manager_server_response})

def admin_add_manager(request):
    admin_username = request.session.get('admin_username')
    admin_email = request.session.get('admin_email')
    if not admin_username or not admin_email:
        return redirect('/admin_login')
    if request.method == 'POST':
        manager_data = {'managerid':request.POST.get('manager_userid'), 'fullname':request.POST.get('manager_fullname')
                         ,'deptname':request.POST.get('manager_deptname'), 'email':request.POST.get('manager_email')
                         ,'mobile':request.POST.get('manager_mobile'),'password':request.POST.get('manager_password')}
        add_manager = requests.post('http://127.0.0.1:8000/managers', json=manager_data)
        if add_manager.status_code == 201:
            # If successful, display success message and pass a redirect flag
            messages.success(request, 'Manager added successfully')
            return redirect('/admin_view_manager_detail')        
        else:
            # If failed, display error message and stay on the same page
            messages.error(request, 'Manager adding failed. Please try again.')
            return redirect('/admin_view_manager_detail') 
    return render(request,'feedbackapp/admin_add_manager.html')

def admin_update_manager(request):
    admin_username = request.session.get('admin_username')
    admin_email = request.session.get('admin_email')
    if not admin_username or not admin_email:
        return redirect('/admin_login')
    
    manager_id = request.GET.get('q')
    fatch_manager_data = requests.get(f'http://127.0.0.1:8000/managers/{manager_id}')
    manager_data_response = fatch_manager_data.json()
    
    if request.method == 'POST':
        manager_data = {'managerid':request.POST.get('manager_userid'), 'fullname':request.POST.get('manager_fullname')
                         ,'deptname':request.POST.get('manager_deptname'), 'email':request.POST.get('manager_email')
                         ,'mobile':request.POST.get('manager_mobile'),'password':request.POST.get('manager_password')}
        print(manager_data)
        add_manager = requests.put(f'http://127.0.0.1:8000/managers/{manager_id}',manager_data)
        
        if add_manager.status_code == 200:
            manager_userid = request.session.get("manager_userid")
            if manager_userid == manager_data_response.get('managerid'):
                # Log out the manager by clearing their session
                if 'manager_id' in request.session:
                    del request.session['manager_id']
                if 'manager_userid' in request.session:
                    del request.session['manager_userid']
                if 'manager_fullname' in request.session:
                    del request.session['manager_fullname']
                if 'manager_email' in request.session:
                    del request.session['manager_email']
            # If successful, display success message and pass a redirect flag
            messages.success(request, 'Manager Update successfully')
            return redirect('/admin_view_manager_detail')
        else:
            # If failed, display error message and stay on the same page
            messages.error(request, 'Manager Updation failed. Please try again.')
            return redirect('/admin_view_manager_detail')
    return render(request,'feedbackapp/admin_update_manager.html',{'manager_key':manager_data_response})

def admin_delete_manager(request):
    admin_username = request.session.get('admin_username')
    admin_email = request.session.get('admin_email')
    if not admin_username or not admin_email:
        return redirect('/admin_login')
    
    manager_id = request.GET.get('q')
    fatch_manager_data = requests.get(f'http://127.0.0.1:8000/managers/{manager_id}')
    manager_data_response = fatch_manager_data.json()
    
    if request.method == 'POST': 
        delete_manager = requests.delete(f'http://127.0.0.1:8000/managers/{manager_id}')
        if delete_manager.status_code == 204:
            manager_userid = request.session.get('manager_userid')
            if manager_userid == manager_data_response.get('managerid'):
                # Log out the manager by clearing their session
                if 'manager_id' in request.session:
                    del request.session['manager_id']
                if 'manager_userid' in request.session:
                    del request.session['manager_userid']
                if 'manager_fullname' in request.session:
                    del request.session['manager_fullname']
                if 'manager_email' in request.session:
                    del request.session['manager_email']
            messages.success(request, 'Manager Deleted successfully')
            return redirect('/admin_view_manager_detail')
        else:
            messages.error(request,"Manager Deletion Failed")
            return redirect('/admin_view_manager_detail')
    return render(request,'feedbackapp/admin_delete_manager.html',{'manager_key':manager_data_response})

def manager_register(request):
    if request.method == 'POST':
        post_manager_Data = {'managerid':request.POST.get('manager_userid'), 'fullname':request.POST.get('manager_fullname')
                         ,'deptname':request.POST.get('manager_deptname'), 'email':request.POST.get('manager_email')
                         ,'mobile':request.POST.get('manager_mobile'),'password':request.POST.get('manager_password')}
        manager_register = requests.post('http://127.0.0.1:8000/managers', json=post_manager_Data)
        if manager_register.status_code == 201:
            messages.success(request,'Manager Registered Successfully')
            return redirect('/manager_login')
        else:
            messages.error(request,'Manager Registration failed')
            return redirect('/manager_register')
    return render(request,'feedbackapp/manager_register.html')

def manager_login(request):
    if request.method == 'POST':
        manager_email = request.POST.get('manager_email')
        manager_password = request.POST.get('manager_password')
        if not manager_email or not manager_password:
            messages.error(request, 'Email and Password are required!')
            return render(request,'feedbackapp/manager_login.html')
        data = {'email': manager_email}
        manager_data = requests.get('http://127.0.0.1:8000/managers',params=data)
        manager_data_response = manager_data.json()
        manager = None
        for m in manager_data_response:
            if m['email']==manager_email:
                if manager_password == m['password']:
                    manager = m
                break
        if manager:
            request.session['manager_id'] = manager['id']
            request.session['manager_userid'] = manager['managerid']
            request.session['manager_fullname'] = manager['fullname']
            request.session['manager_email'] = manager['email']
            messages.success(request,"Login Successfull")
            return redirect('/manager_choice')
        else:
            messages.error(request, 'Invalid Email And Password')
            return redirect('/manager_login')
    return render(request,'feedbackapp/manager_login.html')

def manager_choice(request):
    manager_userid = request.session.get('manager_userid')    
    manager_email = request.session.get('manager_email')
    if not manager_userid or not manager_email:
        return redirect('/manager_login')
    return render(request,'feedbackapp/manager_choice.html',{'manager_userid':manager_userid})

def manager_view_feedback(request):
    manager_userid = request.session.get('manager_userid')
    manager_email = request.session.get('manager_email')
    
    if not manager_userid or not manager_email:
        return redirect('/manager_login')
    
    # Fetch feedback data
    manager_get_feedbacks = requests.get('http://127.0.0.1:8000/feedback')
    
    if manager_get_feedbacks.status_code == 200:
        manager_view_feedback = manager_get_feedbacks.json()
    else:
        manager_view_feedback = []

    # Fetch replies for each feedback
    for feedback in manager_view_feedback:
        feedback_id = feedback['id']
        
        # Fetch replies related to this feedback
        reply_response = requests.get(f'http://127.0.0.1:8000/reply/by_feedback?feedback={feedback_id}')
        
        if reply_response.status_code == 200:
            replies = reply_response.json()
            if replies:
                feedback['reply'] = replies[0]  # Get the first reply (assuming 1:1 relation)
            else:
                feedback['reply'] = None
        else:
            feedback['reply'] = None

    return render(request, 'feedbackapp/manager_view_feedback.html', {'manager_view_feedback': manager_view_feedback})




def manager_reply_feedback(request):
    manager_userid = request.session.get('manager_userid')    
    manager_email = request.session.get('manager_email')
    manager_id = request.session.get('manager_id')
    
    if not manager_userid or not manager_email:
        return redirect('/manager_login')
    
    # Get the feedback id and feedback reply from URL parameters (from Form tag name attribute)
    feedback_front_id = request.GET.get('q')
    feedback_reply = request.POST.get('feedreply')
    # Data fatching from server
    fatch_feedback_id = requests.get(f'http://127.0.0.1:8000/feedback/{feedback_front_id}')
    feedback_data = fatch_feedback_id.json()
    cust_id_from_feedback_data = feedback_data['custid']
    
    fatch_customer_userid = requests.get(f'http://127.0.0.1:8000/customer/{cust_id_from_feedback_data}')
    customer_data = fatch_customer_userid.json()
    
    if request.method == 'POST':
        reply_data = {'custid':cust_id_from_feedback_data ,'feedback':feedback_front_id ,
                  'managerid':manager_id,'replymessage':feedback_reply}
        reply_feedback = requests.post('http://127.0.0.1:8000/reply', data=reply_data)
        if reply_feedback.status_code == 201:
            messages.success(request, 'Reply submitted successfully')
            return redirect('/manager_view_feedback')
        else:
            messages.error(request, 'Reply submission failed')
            return redirect('/manager_view_feedback')      
    return render(request,'feedbackapp/manager_reply_feedback.html',{'feedback_data':feedback_data,'cust_userid':customer_data})

def manager_search_feedback(request):
    manager_userid = request.session.get('manager_userid')    
    manager_email = request.session.get('manager_email')
    if not manager_userid or not manager_email:
        return redirect('/manager_login')
    return render(request,'feedbackapp/manager_search_feedback.html')

def customer_register(request):
    if request.method == 'POST':
        cust_data = {'custid': request.POST.get('customer_userid'),'email': request.POST.get('customer_email'),
                'password': request.POST.get('customer_password'),'mobileno': request.POST.get('customer_mobile'),}
        print(cust_data)
        cust_reg_response = requests.post('http://127.0.0.1:8000/customer', json=cust_data)
        print(cust_reg_response)
        regmsg=''
        if cust_reg_response.status_code == 201:
            messages.success(request, "Customer Registerd Successfully ")
            return redirect('/customer_login')
        else:
            messages.error(request, "Customer Registration Failed ")
            return redirect('/customer_register')
    return render(request,'feedbackapp/customer_register.html')
    
def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('customeremail')
        password = request.POST.get('customerpassword')
        if not email or not password:
            messages.error(request, "Please Enter Login Credentials")
            return redirect('/customer_login')
        data = {'email': email}
        cust_login = requests.get('http://127.0.0.1:8000/customer',params=data)
        cust_login_response = cust_login.json()
        user = None
        for u in cust_login_response:
            if u['email'] == email:
                if password == u['password']:
                    user = u
                break
        if user:
            request.session['customer_email'] = user['email']
            request.session['customer_custid'] = user['custid']
            request.session['customer_id'] = user['id']
            messages.success(request,"Login Successfull")
            return redirect('customer_choice')
        else:
            messages.error(request, "Invalid Email And Password")
            return redirect('/customer_login')
    return render(request,'feedbackapp/customer_login.html')


def customer_choice(request):
    customer_username = request.session.get('customer_custid')
    customer_id = request.session.get('customer_id')
    customer_email = request.session.get('customer_email')
    if not customer_username or not customer_email:
        return redirect('/customer_login')
    return render(request,'feedbackapp/customer_choice.html',{'cust_user':customer_username})


def customer_submit_feedback(request):
    customer_username = request.session.get('customer_custid')
    customer_id = request.session.get('customer_id')
    customer_email = request.session.get('customer_email')
    if not customer_username or not customer_email:
        return redirect('/customer_login')
    if request.method == 'POST':
        feed_data = {'custid':customer_id,'feeddesc':request.POST.get('feeddesc')
                         ,'feedrate':request.POST.get('feedrate')}
        feed_data_response = requests.post('http://127.0.0.1:8000/feedback', json=feed_data)
        if feed_data_response.status_code == 201:
            messages.success(request, 'Feedback submitted successfully')
            return redirect('/customer_view_feedback')
        else:
            messages.error(request, 'Feedback submission failed : {feed_data_response.text}') 
            return redirect('/customer_submit_feedback')       
    return render(request,'feedbackapp/customer_submit_feedback.html',{'cust_id':customer_id,'cust_user':customer_username})

def customer_view_feedback(request):
    customer_username = request.session.get('customer_custid')
    customer_id = request.session.get('customer_id')
    customer_email = request.session.get('customer_email')
    if not customer_username or not customer_email:
        return redirect('/customer_login')
    get_data = requests.get('http://127.0.0.1:8000/feedback')
    fatch_data = get_data.json()
    cust_feedbacks = []
    for i in fatch_data:
        if i['custid'] == customer_id:
            cust_feedbacks.append(i)
    return render(request,'feedbackapp/customer_view_feedback.html',{'cust_data': cust_feedbacks,'cust_user':customer_username})

def cust_edit_feedback(request):
    customer_username = request.session.get('customer_custid')
    customer_id = request.session.get('customer_id')
    customer_email = request.session.get('customer_email')
    if not customer_username or not customer_email:
        return redirect('/customer_login')
    id = request.GET.get('q')
    get_cust_feedback = requests.get('http://127.0.0.1:8000/feedback/'+id)
    fatched_data = get_cust_feedback.json()
    edit_feed_data = {'custid':customer_id,'feeddesc':request.POST.get('feeddesc')
                         ,'feedrate':request.POST.get('feedrate')}
    if request.method == 'POST':
        edit_cust_feedback = requests.put('http://127.0.0.1:8000/feedback/'+id, json=edit_feed_data)
        if edit_cust_feedback.status_code == 200:
            messages.success(request, 'Feedback successfully Edited')
            return redirect('/customer_view_feedback')
        else:
            messages.error(request, 'Feedback Edition failed') 
            return redirect('/customer_view_feedback')
    return render(request,'feedbackapp/cust_edit_feedback.html',{'cust_info':fatched_data,'customer_username':customer_username})

def cust_delete_feedback(request):
    customer_username = request.session.get('customer_custid')
    customer_id = request.session.get('customer_id')
    customer_email = request.session.get('customer_email')
    if not customer_username or not customer_email:
        return redirect('/customer_login')
    id = request.GET.get('q')
    get_cust_feedback = requests.get('http://127.0.0.1:8000/feedback/'+id)
    fatched_data = get_cust_feedback.json()
    if request.method == 'POST':
        delete_cust_feedback = requests.delete('http://127.0.0.1:8000/feedback/'+id)
        if delete_cust_feedback.status_code == 204:
            messages.success(request, 'Feedback successfully Deleted')
            return redirect('/customer_view_feedback')
        else:
            messages.error(request, 'Feedback deletetion failed') 
            return redirect('/customer_view_feedback')
    return render(request,'feedbackapp/cust_delete_feedback.html',{'cust_info':fatched_data,'customer_username':customer_username})

def customer_view_feedback_reply(request):
    # Get logged-in customer details from the session
    customer_username = request.session.get('customer_custid')
    customer_id = request.session.get('customer_id')
    customer_email = request.session.get('customer_email')

    # Redirect if the customer is not logged in
    if not customer_username or not customer_email:
        return redirect('/customer_login')
    customer_get_feedbacks = requests.get(f'http://127.0.0.1:8000/reply')
    if customer_get_feedbacks.status_code == 200:
        # Filter replies to show only for the logged-in customer
        all_replies = customer_get_feedbacks.json()
        customer_view_feedback = []
        for reply in all_replies:
            if reply['custid'] == customer_id:
                customer_view_feedback.append(reply)
    else:
        customer_view_feedback = None
    return render(request, 'feedbackapp/customer_view_feedback_reply.html',{'reply_detail':customer_view_feedback})

def review(request):  
    feed_data_response = requests.get('http://127.0.0.1:8000/reply')
    if feed_data_response.status_code == 200:
        view_feed_data = feed_data_response.json()
    else:
        view_feed_data = None
    return render(request,'feedbackapp/review.html',{'view_feed_data':view_feed_data})

def admin_logout(request):
    # Clear all session data related to the manager
    if 'admin_id' in request.session:
        del request.session['admin_id']
    if 'admin_username' in request.session:
        del request.session['admin_username']
    if 'admin_fullname' in request.session:
        del request.session['admin_fullname']
    if 'admin_email' in request.session:
        del request.session['admin_email']
    return redirect('/admin_login')

def manager_logout(request):
    # Clear all session data related to the manager
    if 'manager_id' in request.session:
        del request.session['manager_id']
    if 'manager_userid' in request.session:
        del request.session['manager_userid']
    if 'manager_fullname' in request.session:
        del request.session['manager_fullname']
    if 'manager_email' in request.session:
        del request.session['manager_email']
    return redirect('/manager_login')

def customer_logout(request):
    # Clear all session data related to the customer
    if 'customer_email' in request.session:
        del request.session['customer_email']
    if 'customer_custid' in request.session:
        del request.session['customer_custid']
    if 'customer_id' in request.session:
        del request.session['customer_id']
    return redirect('/customer_login')

