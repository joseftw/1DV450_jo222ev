class TicketsController < ApplicationController
  #Kontrollerar inloggningen
  before_filter :check_login
  
  def show
    @tickets = Ticket.where("project_id = ?", params[:id])
  end
  
  def create
    @ticket = Ticket.new(params[:ticket])
    @ticket.user_id = session[:user_id]
    
    @ticket = Ticket.new(params[:ticket])
    @ticket.user_id = session[:user_id]
    if @ticket.save
      redirect_to :controller => "projects", :action => "show", :id => @ticket.project_id
    else
      render :action => 'new'
    end


  end
  
  def new
    @ticket = Ticket.new
  end
  
end
