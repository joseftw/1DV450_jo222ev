class Ticket < ActiveRecord::Base
  belongs_to :user
  belongs_to :project
  belongs_to :status
  
  attr_accessible :name, :description, :status_id, :project_id
  
end
