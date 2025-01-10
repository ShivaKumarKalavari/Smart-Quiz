from django.urls import path
from . import views

urlpatterns = [
    # path("todos/",views.todos, name="Todos"),
    #home or login_page
    path("", views.user_login, name="login"),

    #user and admin pages
    path("userMenu/",views.user_menu,name="userMenu"),
    path("adminMenu/",views.admin_menu,name="adminMenu"),

    #User Pages
    path('quiz/<int:quiz_id>/take/',views.take_quiz,name="take_quiz"),
    path('quiz/<int:quiz_id>/submit/',views.submit_quiz,name="submit_quiz"),
    path("results/",views.results_view,name="results"),
    path("execute/",views.execute_code,name="execute_code")
]