class CreateProjectsUsersTable < ActiveRecord::Migration
  #Skapar relationstabellen, primärnyckel skapas inte med flaggan id => false
  def up
    create_table :projects_users, :id => false do |t|

     t.integer "ticket_id"
     t.integer "project_id"
  end
  add_index :projects_users, ["ticket_id", "project_id"]
end
  #Körs vid migrate
  def down
    drop_table :projects_users
  end
end
