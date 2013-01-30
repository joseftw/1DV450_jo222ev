class UsersController < ApplicationController
  #Kontrollerar inloggningen
  before_filter :check_login
  
  def index
    @Users = User.all
  end
  
  def show
    @UserId = params[:id]
    @User = User.find(@UserId)
  end
  
  def new
    
  end
  
  def create
  
  end
  
  def edit
    
  end
  
  def update
    
  end
  
  def destroy
    
  end
  
end
