class UsersController < ApplicationController
  
  def show
    @UserId = params[:id]
    @User = User.find(@UserId)
  end
  
end
