class AddIndexToProjectTable < ActiveRecord::Migration
  def change
    add_index('projects', 'users_id')
  end
end
