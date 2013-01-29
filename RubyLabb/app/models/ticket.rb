class Ticket < ActiveRecord::Base
  belongs_to :users
  belongs_to :projects
  belongs_to :status
end
