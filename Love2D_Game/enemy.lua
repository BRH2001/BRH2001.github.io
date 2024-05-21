local enemies = {}

function spawnEnemy(x, y)
    local enemy = world:newRectangleCollider(x, y, 32, 32, {collision_class = 'Danger'})
    enemy.speed = 100
    enemy.direction = 1
    table.insert(enemies, enemy)
end

function enemiesUpdate(dt)
    for _, enemy in ipairs(enemies) do
        local ex, ey = enemy:getPosition()
        local vx, vy = enemy:getLinearVelocity()

        enemy:applyForce(enemy.speed * enemy.direction, 0)

        if ex < 0 or ex > love.graphics.getWidth() - 32 then
            enemy.direction = -enemy.direction
        end
    end
end

function drawEnemies()
    for _, enemy in ipairs(enemies) do
        local ex, ey = enemy:getPosition()
        love.graphics.setColor(1, 0, 0)
        love.graphics.rectangle('fill', ex - 16, ey - 16, 32, 32)
    end
end