from com.xebialabs.deployit.security.authentication import UserAlreadyExistsException

print "Creating user kate"
try:
    security.createUser('kate', 'k3t3')
except:
    pass

security.assignRole('rest-o-rant-developer', ['kate'])
security.grant('login', 'rest-o-rant-developer')

print "Creating directory Applications/Food"
applicationsHome = 'Applications/Food'
repository.create(factory.configurationItem(applicationsHome, 'core.Directory'))
security.grant('import#initial', 'rest-o-rant-developer', [applicationsHome])
security.grant('import#upgrade', 'rest-o-rant-developer', [applicationsHome])
security.grant('read', 'rest-o-rant-developer', [applicationsHome])

print "Creating directory Environments/FoodCloud"
environmentsHome = 'Environments/FoodCloud'
repository.create(factory.configurationItem(environmentsHome, 'core.Directory'))
security.grant('deploy#initial', 'rest-o-rant-developer', [environmentsHome])
security.grant('deploy#upgrade', 'rest-o-rant-developer', [environmentsHome])
security.grant('deploy#undeploy', 'rest-o-rant-developer', [environmentsHome])
security.grant('read', 'rest-o-rant-developer', [environmentsHome])
security.grant('repo#edit', 'rest-o-rant-developer', [environmentsHome])

print "Creating directory Infrastructure/Cloud"
infrastructureHome = 'Infrastructure/Cloud'
repository.create(factory.configurationItem(infrastructureHome, 'core.Directory'))
security.grant('read', 'rest-o-rant-developer', [infrastructureHome])
security.grant('repo#edit', 'rest-o-rant-developer', [infrastructureHome])
