class HomeController < ApplicationController
  #Kontrollerar inloggningen
  before_filter :check_login
  def index
     
  end

end