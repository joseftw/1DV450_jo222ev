class TicketsController < ApplicationController
  #Kontrollerar inloggningen
  before_filter :check_login
  
  def show
    @tickets = Ticket.where("project_id = ?", params[:id])
  end
  
end
