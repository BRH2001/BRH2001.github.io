function love.load()
    love.window.setMode(800, 600)
    love.window.setTitle("Orb Dodger")

    player = {
        x = 400,
        y = 300,
        radius = 20,
        speed = 300,
        direction = {x = 0, y = 1},
        health = 3,
        maxHealth = 3
    }

    coins = {}
    for i = 1, 10 do
        table.insert(coins, {
            x = love.math.random(50, love.graphics.getWidth() - 50),
            y = love.math.random(50, love.graphics.getHeight() - 50),
            radius = 10
        })
    end

    enemies = {}
    for i = 1, 10 do
        table.insert(enemies, {
            x = love.math.random(50, love.graphics.getWidth() - 50),
            y = love.math.random(50, love.graphics.getHeight() - 50),
            radius = 15,
            speed = 150,
            direction = love.math.random() < 0.5 and {x = 1, y = 0} or {x = -1, y = 0}
        })
    end

    gameState = "menu"
    coinsCollected = 0
    highScore = 0
    pause = false
end

function love.update(dt)
    if gameState == "play" then
        if not pause then
            for _, enemy in ipairs(enemies) do
                enemy.x = enemy.x + enemy.velocityX * dt
                enemy.y = enemy.y + enemy.velocityY * dt

                if enemy.x < 0 then
                    enemy.x = 0
                    enemy.velocityX = -enemy.velocityX
                elseif enemy.x > love.graphics.getWidth() then
                    enemy.x = love.graphics.getWidth()
                    enemy.velocityX = -enemy.velocityX
                end

                if enemy.y < 0 then
                    enemy.y = 0
                    enemy.velocityY = -enemy.velocityY
                elseif enemy.y > love.graphics.getHeight() then
                    enemy.y = love.graphics.getHeight()
                    enemy.velocityY = -enemy.velocityY
                end
            end
        end
    end
end

function love.draw()
    love.graphics.clear(0, 0, 0)

    if gameState == "menu" then
        love.graphics.print("Press SPACE to Start", 300, 280)
    elseif gameState == "play" then
        -- Draw player
        love.graphics.setColor(0, 255, 255)
        drawShadedCircle(player.x, player.y, player.radius, {0, 255, 255}, {0, 200, 200})

        -- Draw coins
        love.graphics.setColor(255, 215, 0)
        for _, coin in ipairs(coins) do
            love.graphics.circle("fill", coin.x, coin.y, coin.radius)
        end

        -- Draw enemies
        love.graphics.setColor(255, 0, 0)
        for _, enemy in ipairs(enemies) do
            love.graphics.circle("fill", enemy.x, enemy.y, enemy.radius)
        end

        -- Draw HUD
        love.graphics.setColor(255, 255, 255)
        love.graphics.print("Coins: " .. coinsCollected, 10, 10)
        love.graphics.print("Health: " .. player.health, 10, 30)
        love.graphics.print("High Score: " .. highScore, 10, 50)
    elseif gameState == "game_over" then
        love.graphics.print("Game Over", 300, 280)
        love.graphics.print("High Score: " .. highScore, 300, 300)
        love.graphics.print("Press SPACE to Try Again", 300, 320)
    end

    if pause then
        love.graphics.print("Paused", 300, 280)
    end
end

function love.keypressed(key)
    if key == "space" then
        if gameState == "menu" or gameState == "game_over" then
            gameState = "play"
            player.x = 500
            player.y = 400
            player.health = player.maxHealth
            coins = {}
            for i = 1, 20 do
                table.insert(coins, {
                    x = love.math.random(50, love.graphics.getWidth() - 50),
                    y = love.math.random(50, love.graphics.getHeight() - 50),
                    radius = 5
                })
            end
            coinsCollected = 0

            enemies = {}
            for i = 1, 20 do
                table.insert(enemies, {
                    x = love.math.random(50, love.graphics.getWidth() - 50),
                    y = love.math.random(50, love.graphics.getHeight() - 50),
                    radius = 15,
                    speed = 150,
                    direction = love.math.random() < 0.5 and {x = 1, y = 0} or {x = -1, y = 0}
                })
            end
        elseif key == "p" then
            pause = not pause
        end
    end
end

function drawShadedCircle(x, y, radius, color1, color2)
    love.graphics.setColor(color1)
    love.graphics.circle("fill", x, y, radius)
    love.graphics.setColor(color2)
    love.graphics.circle("line", x, y, radius + 1)
end

function checkCollision(x1, y1, r1, x2, y2, r2)
    local distance = ((x2 - x1)^2 + (y2 - y1)^2)^0.5
    return distance < r1 + r2
end
