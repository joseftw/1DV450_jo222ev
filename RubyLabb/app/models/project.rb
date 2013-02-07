class Project < ActiveRecord::Base
  has_and_belongs_to_many :users
  has_many :tickets, :dependent => :delete_all
  
  attr_accessible :name, :description, :start_date, :end_date
  
  validates :name,
            :presence => { :message => "Add a name for the project please"},
            :length => { :minimum => 3, :message => "The name must be at least 3 charachters"}
            
  validates :description,
  :presence => { :message => "Add a description for the project please"},
  :length => { :minimum => 50, :message => "The description must be at least 50 charachters" }

  
end
