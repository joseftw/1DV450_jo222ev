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

end
