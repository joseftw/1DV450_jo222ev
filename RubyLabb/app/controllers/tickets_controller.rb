class TicketsController < ApplicationController
  #Kontrollerar inloggningen
  before_filter :check_login
  
  def index
    @project = Project.find(params[:id])
    @tickets = Ticket.where("project_id = ?", params[:id])
  end
  
  def show
    @ticket= Ticket.find(params[:id])
    @project = Project.find(@ticket.project_id)
    @user = User.find(@ticket.user_id)
    @status = Status.find(@ticket.status_id)
  end
  
  def create
    @ticket = Ticket.new(params[:ticket])
    @ticket.user_id = session[:user_id]
    
    @ticket = Ticket.new(params[:ticket])
    @ticket.user_id = session[:user_id]
    if @ticket.save
      redirect_to projects_path
    else
      render :action => 'new'
    end


  end
  
  def new
    @ticket = Ticket.new
  end
  
  def destroy
    #Kolla så att inloggad användare stämmer överrens med ägaren.
    @ticket = Ticket.find(params[:id])
    @project = Project.find(@ticket.project_id) 
    if @ticket.user_id == session[:user_id] || session[:user_id] == @project.user_id
       @ticket.destroy()
      flash[:notice] = "The ticket has been removed"
      redirect_to projects_path
    else
      flash[:error] = "The ticket couldn't be removed, are you sure you are the owner?"
      render :action => 'index'
    end

  end
  
  def edit
    
    @ticket = Ticket.find(params[:id])
  end
  
  def update
    
    @ticket = Ticket.find(params[:id])
    if @ticket.update_attributes(params[:ticket])
      flash[:notice] = "Ticket saved."
      redirect_to :controller=> "projects", :action => "show", :id => @ticket.project_id
    else
      render :action => "edit"
    end
    
  end

  
end
