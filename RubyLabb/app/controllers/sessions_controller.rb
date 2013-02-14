class SessionsController < ApplicationController
  
  def login
  end
  
  def login_attempt
    user = User.authenticate(params[:email], params[:password])
    #Om användaren är godkänd
    if user
      #Spara i session
      session[:user_id] = user.id
      session[:user_first_name] = user.first_name
      flash[:notice] = "Welcome " + user.first_name
      redirect_to(:controller => 'projects')
    else
      flash[:error] = "Invalid email or password"
      flash[:color] = "Invalid"
      render "login"
    end
  end
  
  def logout
    reset_session
    flash[:notice] = "You have successfully logged out"
    redirect_to :action => "login"
  end
  
end
