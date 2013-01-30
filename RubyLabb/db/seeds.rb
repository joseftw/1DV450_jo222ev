# encoding: utf-8
# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

p1 = Project.new
p1.name = "Hack Facebook"
p1.description = "We like Twitter, not Facebook, let's destroy it"
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

s1 = Status.new
s1.status_name = "Fixed";
s1.save

s2 = Status.new
s2.status_name = "Critical"
s2.save

s3 = Status.new
s3.status_name = "Low priority"
s3.save 

s4 = Status.new
s4.status_name = "Will not fix"
s4.save

t1 = Ticket.new
t1.name = "Hacking problem"
t1.description = "It seems like Facebook has very high security"
t1.save

t2 = Ticket.new
t2.name = "Not enough money"
t2.description = "iMacs are more expensive than we first thought, give me some money!"
t2.save

t1.user = u1
t1.project = p1
t1.status = s3

t2.user = u2
t2.project = p2
t2.status = s3

t1.save
t2.save