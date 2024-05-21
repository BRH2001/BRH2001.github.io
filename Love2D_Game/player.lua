local player

function spawnPlayer(x, y)
    player = world:newRectangleCollider(x, y, 32, 64, {collision_class = 'Player'})
    player.speed = 200
    player.isOnGround = false
end

function playerUpdate(dt)
    local px, py = player:getPosition()
    local vx, vy = player:getLinearVelocity()

    if love.keyboard.isDown('left') then
        player:applyForce(-player.speed, 0)
    elseif love.keyboard.isDown('right') then
        player:applyForce(player.speed, 0)
    else
        player:applyForce(0, 0)
    end

    if py > love.graphics.getHeight() - 64 then
        player.isOnGround = true
    else
        player.isOnGround = false
    end
end

function drawPlayer()
    local px, py = player:getPosition()
    love.graphics.setColor(1, 1, 1)
    love.graphics.rectangle('fill', px - 16, py - 32, 32, 64)
end