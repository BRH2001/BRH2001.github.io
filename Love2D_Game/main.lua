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

    -- Add 6 new diagonal enemies
    for i = 1, 6 do
        table.insert(enemies, {
            x = love.math.random(50, love.graphics.getWidth() - 50),
            y = love.math.random(50, love.graphics.getHeight() - 50),
            radius = 15,
            speed = 150,
            direction = {
                x = love.math.random() < 0.5 and 1 or -1,
                y = love.math.random() < 0.5 and 1 or -1
            }
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
            if love.keyboard.isDown("up", "w") then
                player.y = player.y - player.speed * dt
            elseif love.keyboard.isDown("down", "s") then
                player.y = player.y + player.speed * dt
            end

            if love.keyboard.isDown("left", "a") then
                player.x = player.x - player.speed * dt
            elseif love.keyboard.isDown("right", "d") then
                player.x = player.x + player.speed * dt
            end

            if player.x < player.radius then
                player.x = player.radius
            elseif player.x > love.graphics.getWidth() - player.radius then
                player.x = love.graphics.getWidth() - player.radius
            end

            if player.y < player.radius then
                player.y = player.radius
            elseif player.y > love.graphics.getHeight() - player.radius then
                player.y = love.graphics.getHeight() - player.radius
            end

            for _, enemy in ipairs(enemies) do
                enemy.x = enemy.x + enemy.speed * enemy.direction.x * dt
                enemy.y = enemy.y + enemy.speed * enemy.direction.y * dt

                if enemy.x < enemy.radius or enemy.x > love.graphics.getWidth() - enemy.radius then
                    enemy.direction.x = -enemy.direction.x
                end

                if enemy.y < enemy.radius or enemy.y > love.graphics.getHeight() - enemy.radius then
                    enemy.direction.y = -enemy.direction.y
                end

                if checkCollision(player.x, player.y, player.radius, enemy.x, enemy.y, enemy.radius) then
                    player.health = player.health - 1
                    if player.health <= 0 then
                        gameState = "game_over"
                        highScore = math.max(highScore, coinsCollected)
                    end
                end
            end

            for i, coin in ipairs(coins) do
                if checkCollision(player.x, player.y, player.radius, coin.x, coin.y, coin.radius) then
                    table.remove(coins, i)
                    coinsCollected = coinsCollected + 1
                end
            end
        end
    end
end

function love.draw()
    love.graphics.clear(0, 0, 0)

    if gameState == "menu" then
        love.graphics.print("Press SPACE to Start", 462, 384)
    elseif gameState == "play" then
        love.graphics.setColor(0, 255, 255)
        drawShadedCircle(player.x, player.y, player.radius, {0, 255, 255}, {0, 200, 200})

        love.graphics.setColor(255, 215, 0)
        for _, coin in ipairs(coins) do
            love.graphics.circle("fill", coin.x, coin.y, coin.radius)
        end

        love.graphics.setColor(255, 0, 0)
        for _, enemy in ipairs(enemies) do
            love.graphics.circle("fill", enemy.x, enemy.y, enemy.radius)
        end

        love.graphics.setColor(255, 255, 255)
        love.graphics.print("Coins: " .. coinsCollected, 10, 10)
        love.graphics.print("Health: " .. player.health, 10, 30)
        love.graphics.print("High Score: " .. highScore, 10, 50)
    elseif gameState == "game_over" then
        love.graphics.print("Game Over", 462, 384)
        love.graphics.print("High Score: " .. highScore, 462, 404)
        love.graphics.print("Press SPACE to Try Again", 462, 424)
    end

    if pause then
        love.graphics.print("Paused", 462, 384)
    end
end

function love.keypressed(key)
    if key == "space" then
        if gameState == "menu" or gameState == "game_over" then
            gameState = "play"
            player.x = 512
            player.y = 384
            player.health = player.maxHealth
            coins = {}
            for i = 1, 20 do
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
            for i = 1, 10 do
                table.insert(enemies, {
                    x = love.math.random(50, love.graphics.getWidth() - 50),
                    y = love.math.random(50, love.graphics.getHeight() - 50),
                    radius = 15,
                    speed = 150,
                    direction = love.math.random() < 0.5 and {x = 0, y = 1} or {x = 0, y = -1}
                })
            end

            coinsCollected = 0
            pause = false
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
