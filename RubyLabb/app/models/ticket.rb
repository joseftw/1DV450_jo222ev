class Ticket < ActiveRecord::Base
  belongs_to :user
  belongs_to :project
  belongs_to :status
  
  attr_accessible :name, :description, :status_id, :project_id, :ticket_id
  
  validates_presence_of :name, :description
  
  validates :name, :length => { :minimum => 4,
                                :maximum => 50,
                                :too_short => "The name must be at least 4 charachters long.",
                                :too_long => "The name can't be longer than 50 charachters." }
  
  validates :description, :length => { :minimum => 10,
    :maximum => 5000,
    :tokenizer => lambda { |str| str.scan(/\w+/) },
    :too_short => "The description must be at least 10 words.",
    :too_long => "The description can only hold 5000 words." } 
  
end
