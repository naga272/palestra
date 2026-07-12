package main


import (
	"github.com/gin-gonic/gin"
	"github.com/gin-contrib/cors"
	"time"
	"backend/routes"
)


func main() {
	r := gin.Default()
	
	r.Use(cors.New(cors.Config{
		AllowOrigins: []string{"http://localhost:8080"},
		AllowMethods: []string{"GET", "POST"},
		AllowHeaders: []string{"Origin", "Content-Type"},
		ExposeHeaders: []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge: 12 * time.Hour,
	}))

	routes.SetupRoutes(r)

	r.Run(":8000")
}