## Links
https://docs.microsoft.com/en-gb/java/azure/spring-framework/deploy-spring-boot-java-app-with-maven-plugin?view=azure-java-stable
https://github.com/spring-guides/gs-spring-boot
https://spring.io/guides/gs/rest-service/
https://dzone.com/articles/using-the-spring-requestmapping-annotation

## Setting up
Install JDK - https://www.oracle.com/technetwork/java/javase/downloads/index.html

Make sure PATH includes C:\Program Files\Java\jre1.8.0_221\bin (not sure if this is requried)
Make sure JAVA_HOME = C:\Program Files\Java\jdk-13

Install Apache Maven - 
https://maven.apache.org/guides/getting-started/windows-prerequisites.html
https://maven.apache.org/download.cgi

Put this in PATH : C:\Program Files\apache-maven-3.6.2\bin

## To Build
```mvn clean package```

## To Run Locally
```mvn spring-boot:run```

## To Deploy to Azure
```mvn azure-webapp:deploy```

## To reset Powershell console colours if the above mess them up :
```[Console]::ResetColor()```



