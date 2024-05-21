function love.load()
    love.window.setMode(800, 600)

    wf = require 'windfield'

    world = wf.newWorld(0, 800, false)
    world:setQueryDebugDrawing(true)
    world:addCollisionClass('Platform')
    world:addCollisionClass('Player', {ignores = {'Platform'}})
    world:addCollisionClass('Danger')

    require('player')
    require('enemy')

    dangerZone = world:newRectangleCollider(-500, 600, 1800, 50, {collision_class = 'Danger'})
    dangerZone:setType('static')

    player:setFixedRotation(true)

    platforms = {}
    enemies = {}

    flagX = 0
    flagY = 0
    saveData = {currentLevel = "level1"}

    loadMap(saveData.currentLevel)
end

function love.update(dt)
    world:update(dt)
    playerUpdate(dt)
    enemiesUpdate(dt)

    local px, py = player:getPosition()
    cam:lookAt(px, love.graphics.getHeight() / 2)

    local colliders = world:queryCircleArea(flagX, flagY, 10, {'Player'})
    if #colliders > 0 then
        if saveData.currentLevel == "level1" then
            loadMap("level2")
            saveData.currentLevel = "level2"
        elseif saveData.currentLevel == "level2" then
            saveData.currentLevel = "level1"
            loadMap("level1")
        end
    end
end

function love.draw()
    cam:attach()
    drawPlayer()
    drawEnemies()
    cam:detach()
end

function love.keypressed(key)
    if key == 'space' and player.isOnGround then
        player:applyLinearImpulse(0, -4000)
    end
end

function destroyAll()
    for i = #platforms, 1, -1 do
        if platforms[i] ~= nil then
            platforms[i]:destroy()
            table.remove(platforms, i)
        end
    end

    for i = #enemies, 1, -1 do
        if enemies[i] ~= nil then
            enemies[i]:destroy()
            table.remove(enemies, i)
        end
    end
end

function love.mousepressed(x, y, button)
    if button == 1 then
        local colliders = world:queryCircleArea(x, y, 200, {'Platform', 'Danger'})
        for i, c in ipairs(colliders) do
            c:destroy()
        end
    end
end

function spawnPlatform(x, y, width, height)
    if width > 0 and height > 0 then
        local platform = world:newRectangleCollider(x, y, width, height, {collision_class = 'Platform'})
        platform:setType('static')
        table.insert(platforms, platform)
    end
end

function loadMap(mapName)
    saveData.currentLevel = mapName
    destroyAll()

    spawnPlayer(100, 500)

    spawnPlatform(0, 550, 800, 50)
    spawnPlatform(200, 400, 200, 20)
    spawnPlatform(500, 300, 200, 20)

    spawnEnemy(300, 520)
    spawnEnemy(600, 270)

    flagX = 700
    flagY = 270
end