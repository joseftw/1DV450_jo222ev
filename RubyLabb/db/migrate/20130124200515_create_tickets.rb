class CreateTickets < ActiveRecord::Migration
  def change
    create_table :tickets do |t|
      t.references :users
      t.references :tickets
      t.references :status

      t.string :name
      t.string :description
      t.timestamps
    end
  end
end
