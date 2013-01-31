class Project < ActiveRecord::Base
  has_and_belongs_to_many :users
  has_many :tickets
  
  attr_accessible :name, :description, :start_date, :end_date
end
