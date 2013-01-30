class ProjectsController < ApplicationController

  before_filter :check_login
def index
    
    user_id = session[:user_id]
    @projects = Project.all
    @user = User.find(user_id)
   
end

def show
  @projectId = params[:id].to_i 
  @project = Project.find(@projectId)
end

end
