class ProjectsController < ApplicationController
  #Kontrollerar inloggningen
  before_filter :check_login
  def index
      user_id = session[:user_id]
      @projects = Project.all
      @user = User.find(user_id) 
  end
  
  def show
    projectId = params[:id].to_i 
    @project = Project.find(projectId)
    @ticket = Ticket.new
  end
  
  def new
    @project = Project.new
  end
  
  def create
    @project = Project.new(params[:project])
    @project.user_id = session[:user_id]
    if @project.save
      redirect_to projects_path
    else
      render :action => 'new'
    end
  end
  
  def destroy
    #Kolla så att inloggad användare stämmer överrens med ägaren.
    @project = Project.find(params[:id]) 
    if @project.user_id == session[:user_id]
       @project.destroy()
      redirect_to projects_path
    else
      render :action => 'index'
    end

  end
  
  def edit
    render :action => "edit"
  end

end
