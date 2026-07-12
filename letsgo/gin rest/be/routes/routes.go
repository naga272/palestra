package routes

import (
	"github.com/gin-gonic/gin"
	"backend/controller"
)


func SetupRoutes(routes *gin.Engine) {
	api := routes.Group("/api")
	{
		api.GET("/hello", controller.HelloHandler)
	}
}