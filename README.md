# 💫 About Me:
I am currently pursuing my tertiary education at the Sepuluh Nopember Institute of Technology.<br><br>I am interested in several fields to continue to learn, including:<br>Low-Level & Systems Programming<br>Cybersecurity Engineering<br>Backend Engineering<br>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💻 Code Enthusiast</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes code-scroll {
            0% { transform: translateY(0); }
            100% { transform: translateY(-50%); }
        }

        @keyframes glitch {
            0% { text-shadow: 2px 0 #00ff9d, -2px 0 #ff00c1; }
            100% { text-shadow: -2px 0 #00ff9d, 2px 0 #ff00c1; }
        }

        .cyber-terminal {
            background: linear-gradient(45deg, #0a0a0a, #001a0f);
            box-shadow: 0 0 30px #00ff9d33;
        }

        .code-animation {
            animation: code-scroll 20s linear infinite;
            background: repeating-linear-gradient(
                #001a0f,
                #001a0f 24px,
                #00ff9d25 24px,
                #00ff9d25 48px
            );
        }

        .cyber-glitch {
            animation: glitch 0.3s infinite alternate;
        }

        .laptop-body {
            background: linear-gradient(45deg, #1a1a1a, #333);
            border-radius: 8px 8px 0 0;
        }

        .laptop-screen {
            background: radial-gradient(circle, #001a0f 0%, #000 100%);
            box-shadow: inset 0 0 20px #00ff9d33;
        }
    </style>
</head>
<body class="bg-gray-900 min-h-screen flex items-center justify-center overflow-hidden">
    <!-- Animated Code Panel -->
    <div class="fixed left-8 bottom-8 w-64 h-96 cyber-terminal rounded-lg overflow-hidden">
        <div class="code-animation h-[200%] p-4 font-mono text-green-400 text-sm">
            <!-- Generated code will be inserted here -->
        </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-2xl w-full space-y-8 p-8 relative z-30">
        <!-- Visit Counter -->
        <div class="bg-gray-800/90 backdrop-blur rounded-lg p-4 shadow-2xl hover:shadow-green-500/20 transition-all">
            <div class="flex items-center space-x-4">
                <div class="bg-green-500/20 p-3 rounded-full">
                    <div class="w-6 h-6 bg-green-500 rounded-full animate-pulse"></div>
                </div>
                <div>
                    <p class="text-2xl font-bold text-green-400" id="visitCount">0</p>
                    <p class="text-sm text-gray-400">VISITORS COUNT</p>
                </div>
            </div>
        </div>

        <!-- Profile Section -->
        <div class="text-center space-y-6">
            <h1 class="text-5xl font-bold text-green-400 cyber-glitch">CYBER_DEV</h1>
            <p class="text-lg text-gray-300 font-mono">>_ I am developer</p>
        </div>
    </div>

    <!-- 3D Laptop -->
    <div class="fixed right-8 bottom-8 w-96 h-64 laptop-body transform perspective-1000 rotate-x-12">
        <div class="laptop-screen h-full p-4 rounded-t-lg">
            <div class="h-full bg-black/80 rounded overflow-hidden">
                <div class="code-animation h-[200%] p-4 font-mono text-green-400 text-sm">
                    <!-- Generated code will be inserted here -->
                </div>
            </div>
        </div>
        <div class="h-4 bg-gray-800 rounded-b-lg"></div>
    </div>

    <script>
        // Visit Counter
        document.addEventListener('DOMContentLoaded', () => {
            let count = localStorage.getItem('visitCount') || 0;
            count = Number(count) + 1;
            localStorage.setItem('visitCount', count);
            document.getElementById('visitCount').textContent = `0x${count.toString(16).padStart(4, '0')}`;
        });

        // Random Code Generator
        function generateCode(lines = 50) {
            const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$%&/#1234567890{}[]=+-_';
            const commands = ['git commit', 'npm start', 'sudo apt-get', 'docker build', 'curl -X GET'];
            
            return Array.from({length: lines}, (_, i) => {
                if(i % 5 === 0) {
                    return `<span class="text-blue-400">${commands[Math.floor(Math.random() * commands.length)]}</span>`;
                }
                return Array.from({length: 40}, () => 
                    characters[Math.floor(Math.random() * characters.length)]
                ).join('');
            }).join('<br>');
        }

        // Insert generated code to all code panels
        document.querySelectorAll('.code-animation').forEach(panel => {
            panel.innerHTML = generateCode(30);
        });
    </script>
</body>
</html>

# 💻 Tech Stack:
![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white) ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) ![Dart](https://img.shields.io/badge/dart-%230175C2.svg?style=for-the-badge&logo=dart&logoColor=white) ![Go](https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white) ![Kotlin](https://img.shields.io/badge/kotlin-%237F52FF.svg?style=for-the-badge&logo=kotlin&logoColor=white) ![PHP](https://img.shields.io/badge/php-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white) ![Bash Script](https://img.shields.io/badge/bash_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
# 📊 GitHub Stats:
![](https://github-readme-stats.vercel.app/api?username=AtokTajuddin&theme=dark&hide_border=false&include_all_commits=true&count_private=false)<br/>
![](https://nirzak-streak-stats.vercel.app/?user=AtokTajuddin&theme=dark&hide_border=false)<br/>
![](https://github-readme-stats.vercel.app/api/top-langs/?username=AtokTajuddin&theme=dark&hide_border=false&include_all_commits=true&count_private=false&layout=compact)

### 🐍 GitHub Contributions Snake
![GitHub Snake Animation](https://raw.githubusercontent.com/AtokTajuddin/AtokTajuddin/output/github-snake.svg)



# GitHub Activity Graph
[![GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=AtokTajuddin&theme=react-dark&area=true&hide_border=true&custom_title=Contribution%20Graph&line=61DAFB&bg_color=00000000&redirect=true)](https://github.com/AtokTajuddin)
#


### ✍️ Random Dev Quote
![](https://quotes-github-readme.vercel.app/api?type=horizontal&theme=radical)

### 🔝 Top Contributed Repo
![](https://github-contributor-stats.vercel.app/api?username=AtokTajuddin&limit=5&theme=dark&combine_all_yearly_contributions=true)

---
[![](https://visitcount.itsvg.in/api?id=AtokTajuddin&icon=0&color=0)](https://visitcount.itsvg.in)

<!-- Proudly created with GPRM ( https://gprm.itsvg.in ) -->
