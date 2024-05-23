function love.load()
    love.window.setMode(800, 600)
    love.window.setTitle("Orb Dodger")

    player = {
        x = 400,
        y = 300,
        radius = 20,
        speed = 300,
        direction = {x = 0, y = 1},
        invincibility = 1,
        invincible = true
    }

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
            direction = love.math.random() < 0.5 and {x = 1, y = 0} or {x = -1, y = 0},
            color = {255, 0, 0}
        })
    end
    for i = 1, 10 do
        table.insert(enemies, {
            x = love.math.random(50, love.graphics.getWidth() - 50),
            y = love.math.random(50, love.graphics.getHeight() - 50),
            radius = 15,
            speed = 150,
            direction = love.math.random() < 0.5 and {x = 0, y = 1} or {x = 0, y = -1},
            color = {255, 0, 0}
        })
    end
    for i = 1, 6 do
        table.insert(enemies, {
            x = love.math.random(50, love.graphics.getWidth() - 50),
            y = love.math.random(50, love.graphics.getHeight() - 50),
            radius = 15,
            speed = 150,
            direction = {
                x = love.math.random() < 0.5 and 1 or -1,
                y = love.math.random() < 0.5 and 1 or -1
            },
            color = {255, 0, 0}
        })
    end

    gameState = "menu"
    coinsCollected = 0
    highScore = 0
    pause = false
end

function love.update(dt)
    if gameState == "play" then
        if player.invincibility > 0 then
            player.invincibility = player.invincibility - dt
            if player.invincibility <= 0 then
                player.invincible = false
                player.invincibility = 0
            end
        end

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

                if not player.invincible and checkCollision(player.x, player.y, player.radius, enemy.x, enemy.y, enemy.radius) then
                    gameState = "game_over"
                    highScore = math.max(highScore, coinsCollected)
                end
            end

            for i, coin in ipairs(coins) do
                if checkCollision(player.x, player.y, player.radius, coin.x, coin.y, coin.radius) then
                    table.remove(coins, i)
                    coinsCollected = coinsCollected + 1
                end
            end

            if #coins == 0 then
                gameState = "you_win"
                highScore = math.max(highScore, coinsCollected)
            end
        end
    end
end

function love.draw()
    if gameState == "play" then
        love.graphics.setBackgroundColor(0, 0, 0)

        local playerColor = player.invincible and {0, 0, 0} or {0, 0, 255}
        drawShadedCircle(player.x, player.y, player.radius, playerColor, player.invincible and {0, 0, 255})

        love.graphics.setColor(255, 255, 0)
        for _, coin in ipairs(coins) do
            love.graphics.circle("fill", coin.x, coin.y, coin.radius)
        end

        for _, enemy in ipairs(enemies) do
            if enemy.color then
                love.graphics.setColor(enemy.color[1], enemy.color[2], enemy.color[3])
                love.graphics.circle("fill", enemy.x, enemy.y, enemy.radius)
            else
                love.graphics.setColor(255, 0, 0)
                love.graphics.circle("fill", enemy.x, enemy.y, enemy.radius)
            end
        end

        love.graphics.setColor(255, 255, 255)
        love.graphics.print("Coins: " .. coinsCollected, 10, 10)
        love.graphics.print("High Score: " .. highScore, 10, 30)

    else
        love.graphics.setBackgroundColor(0, 0, 0)

        if gameState == "menu" then
            local text = "Press SPACE to Start"
            local font = love.graphics.getFont()
            local textWidth = font:getWidth(text)
            local textHeight = font:getHeight(text)
            love.graphics.setColor(255, 255, 255)
            love.graphics.print(text, (love.graphics.getWidth() - textWidth) / 2, (love.graphics.getHeight() - textHeight) / 2)

        elseif gameState == "game_over" then
            local text1 = "Game Over"
            local text2 = "High Score: " .. highScore
            local text3 = "Press SPACE to Try Again"
            local font = love.graphics.getFont()
            local textWidth1 = font:getWidth(text1)
            local textHeight1 = font:getHeight(text1)
            local textWidth2 = font:getWidth(text2)
            local textHeight2 = font:getHeight(text2)
            local textWidth3 = font:getWidth(text3)
            local textHeight3 = font:getHeight(text3)
            love.graphics.setColor(255, 255, 255)
            love.graphics.print(text1, (love.graphics.getWidth() - textWidth1) / 2, (love.graphics.getHeight() - textHeight1) / 2 - 20)
            love.graphics.print(text2, (love.graphics.getWidth() - textWidth2) / 2, (love.graphics.getHeight() - textHeight2) / 2)
            love.graphics.print(text3, (love.graphics.getWidth() - textWidth3) / 2, (love.graphics.getHeight() - textHeight3) / 2 + 20)

        elseif gameState == "you_win" then
            local text1 = "You Win!"
            local text2 = "High Score: " .. highScore
            local text3 = "Press SPACE to Play Again"
            local font = love.graphics.getFont()
            local textWidth1 = font:getWidth(text1)
            local textHeight1 = font:getHeight(text1)
            local textWidth2 = font:getWidth(text2)
            local textHeight2 = font:getHeight(text2)
            local textWidth3 = font:getWidth(text3)
            local textHeight3 = font:getHeight(text3)
            love.graphics.setColor(255, 255, 255)
            love.graphics.print(text1, (love.graphics.getWidth() - textWidth1) / 2, (love.graphics.getHeight() - textHeight1) / 2 - 20)
            love.graphics.print(text2, (love.graphics.getWidth() - textWidth2) / 2, (love.graphics.getHeight() - textHeight2) / 2)
            love.graphics.print(text3, (love.graphics.getWidth() - textWidth3) / 2, (love.graphics.getHeight() - textHeight3) / 2 + 20)
        end
        if pause then
            local text = "Paused"
            local font = love.graphics.getFont()
            local textWidth = font:getWidth(text)
            local textHeight = font:getHeight(text)
            love.graphics.setColor(255, 255, 255)
            love.graphics.print(text, (love.graphics.getWidth() - textWidth) / 2, (love.graphics.getHeight() - textHeight) / 2)
        end
    end
end

function love.keypressed(key)
    if key == "space" then
        if gameState == "menu" or gameState == "game_over" or gameState == "you_win" then
            gameState = "play"
            player.x = 400
            player.y = 300
            player.invincibility = 1
            player.invincible = true
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
            for i = 1, 6 do
                table.insert(enemies, {
                    x = love.math.random(50, love.graphics.getWidth() - 50),
                    y = love.math.random(50, love.graphics.getHeight() - 50),
                    radius = 15,
                    speed = 150,
                    direction = {
                        x = love.math.random() < 0.5 and 1 or -1,
                        y = love.math.random() < 0.5 and 1 or -1
                    },
                    color = {255, 0, 0}
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
    if color2 then
        love.graphics.setColor(color2)
        love.graphics.circle("line", x, y, radius + 1)
    end
end

function checkCollision(x1, y1, r1, x2, y2, r2)
    local distance = ((x2 - x1)^2 + (y2 - y1)^2)^0.5
    return distance < r1 + r2
end
