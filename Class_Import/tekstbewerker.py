<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>brh2001's Portfolio</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #474747;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    header {
      background-color: #474747;
      background-image: linear-gradient(-45deg, rgba(255, 255, 255, 0.6) 25%, transparent 25%, transparent 75%, rgba(0, 0, 0) 100%), linear-gradient(-45deg, rgba(255, 255, 255, 0.5) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.5) 75%);
      color: #ffffff;
      text-align: center;
      padding: 3px 0;
      flex-shrink: 0;
      font-size: 15px;
      position: relative;
      z-index: 2;
    }

    footer {
      background-color: #474747;
      background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.6) 25%, transparent 25%, transparent 75%, rgba(0, 0, 0) 100%), linear-gradient(45deg, rgba(255, 255, 255, 0.5) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.5) 75%);
      color: #ffffff;
      text-align: center;
      padding: 9px 0;
      flex-shrink: 0;
      position: relative;
      z-index: 2;
    }

    .container {
      max-width: 800px;
      margin: auto;
      padding: 3px;
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      position: relative;
      z-index: 2;
    }

    .projects-container {
      display: flex;
      justify-content: space-between;
      max-width: 800px;
      margin: auto;
    }

    .projects-container ul {
      list-style-type: none;
      padding: 0;
      width: 48%;
    }

    .projects-container li {
      margin-bottom: 10px;
    }

    section {
      text-align: left;
      background-color: rgba(0, 0, 0, 0.555);
      padding: 3px;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(255, 255, 255, 0.3);
      margin-bottom: 3px;
      transition: transform 0.2s;
      position: relative;
      z-index: 2;
      color: #ffffff;
    }

    .projects:hover,
    .about:hover {
      transform: scale(1.05);
    }

    section h2 {
      color: #ffffff;
    }

    section p {
      color: #ffffff;
    }

    section ul {
      list-style-type: none;
      padding: 0;
    }

    section ul li {
      margin-bottom: 10px;
    }

    section ul li a {
      color: #00ffbf;
      text-decoration: none;
    }

    section ul li a:hover {
      text-decoration: underline;
    }

    .logo {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 1;
      width: 582px;
      height: auto;
    }

    .corner-rectangle {
      position: absolute;
      width: 100px;
      height: 100px;
      z-index: 1;
    }

    .top-left {
      top: 0;
      left: 0;
      clip-path: polygon(0 0, calc(100% - 1px) 0, 0 calc(100% - 1px));
      background-color: #000000;
    }

    .bottom-left,
    .top-right {
      background-color: #000000;
    }

    .bottom-right {
      bottom: 0;
      right: 0;
      clip-path: polygon(100% 100%, 0 100%, 100% 0);
      background: linear-gradient(-45deg, rgba(0, 0, 0, 0.6) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.5) 75%);
    }

    @media screen and (max-width: 528px) {
      header h1 {
        font-size: 17px;
      }

      .logo {
        width: 333px;
      }

      .projects-container {
        flex-direction: column;
      }

      .projects-container ul {
        margin: 3px 0;
      }
    }
  </style>
</head>

<body>
  <header>
    <h1>Welkom bij mijn portfolio!</h1>
  </header>
  <div class="container">
    <section class="projects">
      <h2>Projecten</h2>
      <div class="projects-container">
        <ul>
          <li><a href="https://github.com/BRH2001/BRH2001.github.io/tree/main/Mars_Retrieval">Mars_Rover App.</a></li>
          <li><a href="https://github.com/BRH2001/BRH2001.github.io/tree/main/License_Checker">Kenteken_Checker App.</a></li>
          <li><a href="https://github.com/BRH2001/BRH2001.github.io/tree/main/data_transfer">Data_Transfer Project.</a></li>
        </ul>
        <ul>
          <li><a href="https://github.com/BRH2001/BRH2001.github.io/tree/main/Class_Import">Class_Import Project.</a></li>
          <li><a href="https://github.com/BRH2001/BRH2001.github.io/tree/main/Mastermind_Game">Mastermind_Web Game.</a></li>
          <li><a href="https://github.com/BRH2001/BRH2001.github.io/tree/main/Orb-Dodger_Game">Orb_Dodger Game.</a></li>
        </ul>
      </div>
    </section>
    <section class="about">
      <h2>Over mij</h2>
      <p>Ik ben 23 jaar oud en gepassioneerd over softwareontwikkeling.</p>
      <p>Ik studeer aan het Rea College in Groningen, waar ik me specialiseer in het bouwen van innovatieve en
        gebruiksvriendelijke applicaties. Mijn doel is om een ervaren applicatieontwikkelaar te worden.</p>
      <p>Ik streef er naar om zo veel mogelijk te groeien en leren. Aldus werk ik aan verschillende projecten om mijn vaardigheden te verbeteren en nieuwe technologieën te verkennen.</p>
      <p>Deze site biedt een glimps van recente projecten en mijn creatieve benadering van softwareontwikkeling.</p>
      <p>Ik ben enthousiast over de toekomst van technologie en de impact die we kunnen hebben door middel van innovatie.</p>
    </section>
  </div>
  <footer>
    <p>&copy; Bartho Hartjes 2024</p>
  </footer>
  <img src="trinity-web.png" alt="Logo" class="logo">
</body>

</html>
