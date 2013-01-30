class User < ActiveRecord::Base
  has_and_belongs_to_many :projects
  has_many :tickets
  
  attr_accessible :email, :password
  EMAIL_REGEX = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+.[A-Z]{2,4}$/i
  validates :email, presence: true
  validates :password, presence: true
  
  #Metod som ansvarar för autensieringen.
  def self.authenticate(email="", password="")
    if  EMAIL_REGEX.match(email)    
      user = User.find_by_email(email)
    end
  
    if user && user.password == password
      return user
    else
      return false
    end
  
  end

  
end
