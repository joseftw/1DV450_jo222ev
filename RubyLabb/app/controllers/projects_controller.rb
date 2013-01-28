class ProjectsController < ApplicationController

def index
  @projects = Project.all 
end

def show
  @projectId = params[:id].to_i 
  @project = Project.find(@projectId)
end

end
