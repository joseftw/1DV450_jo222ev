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
      flash[:notice] = "Successfully created " + @project.name
      user = User.find(session[:user_id])
      user.projects << @project
      redirect_to projects_path
    else
      flash[:error] = "Could not create project, try again."
      render :action => 'new'
    end
  end
  
  def destroy
    #Kolla så att inloggad användare stämmer överrens med ägaren.
    @project = Project.find(params[:id]) 
    if @project.user_id == session[:user_id]
       @project.destroy()
      flash[:notice] = "Your project has been removed"
      redirect_to projects_path
    else
      flash[:error] = "The project couldn't be removed, are you sure you are the owner?"
      render :action => 'index'
    end

  end
  
  def edit
    @project = Project.find(params[:id])
  end
  
  def update
    @project = Project.find(params[:id])
    if @project.update_attributes(params[:project])
      flash[:notice] = "Project saved."
      redirect_to :controller=> "projects", :action => "show", :id => @project.id
    else
      render :action => "edit"
    end
    
  end
  
  def join
    project = Project.find(params[:id])
    user = User.find(session[:user_id])
    user.projects << project
     
    flash[:notice] = "You have successfully joined the project"
    redirect_to :controller=> "projects", :action => "show", :id => project.id
  end
  
  def leave
    
  end

end
