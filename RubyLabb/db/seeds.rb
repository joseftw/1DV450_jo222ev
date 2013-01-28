# encoding: utf-8
# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

p1 = Project.new
p1.name = "Kill Usama Bin Laden"
p1.description = "We know where he is moahahaha"
p1.start_date = Time.now
p1.end_date = Time.now + (2*7*24*60*60)
p1.save

p2 = Project.new
p2.name = "Buy an iMac"
p2.description = "Finally have all the money in the world..."
p2.start_date = Time.now
p2.end_date = Time.now + (2*7*24*60*60)
p2.save

u1 = User.new
u1.first_name = "Daniel"
u1.last_name = "Toll"
u1.password = "phpMVC<3"
u1.email = "danielToll@lnu.se"
u1.save

u2 = User.new
u2.first_name = "Mark"
u2.last_name = "Zuckerberg"
u2.password = "hateTwitter"
u2.email = "mark@facebook.com"
u2.save

u1.projects << p1
u2.projects << p1
u2.projects << p2