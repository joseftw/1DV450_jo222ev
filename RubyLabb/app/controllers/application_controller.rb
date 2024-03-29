class ApplicationController < ActionController::Base
  protect_from_forgery

  def check_login
    unless session[:user_id]
      redirect_to(:controller => 'sessions', :action => 'login')
      flash[:error] = "You need to be logged in to view this site."
      return false
    else
     return true
     end
  end    
end
