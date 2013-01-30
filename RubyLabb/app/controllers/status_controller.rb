class StatusController < ApplicationController
  #Kontrollerar inloggningen
  before_filter :check_login
  
end
