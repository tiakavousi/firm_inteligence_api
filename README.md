# firm_inteligence_api
GET /health
GET /firms                      # returns every firm
GET /firms/{id}                 # Returns one firm, 404 if not exists
GET /firms/{id}/benchmarks      # Revenue per lawyer , profit per equity partner
POST /firms                   #Add a firm%