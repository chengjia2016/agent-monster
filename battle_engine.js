const CRYPTO = require('crypto');

const BATTLE_TYPES = {
    NORMAL: 'normal',
    CRITICAL: 'critical',
    RAID: 'raid'
};

const ELEMENT_TYPES = {
    LOGIC: { strong: ['CREATIVE'], weak: ['SPEED'] },
    CREATIVE: { strong: ['SPEED'], weak: ['LOGIC'] },
    SPEED: { strong: ['LOGIC'], weak: ['CREATIVE'] }
};

class BattleEngine {
    constructor(mySoul, opponentSoul, commitHash) {
        this.mySoul = mySoul;
        this.opponentSoul = opponentSoul;
        this.commitHash = commitHash;
        this.seed = this.generateSeed();
        this.log = [];
    }

    generateSeed() {
        const data = this.opponentSoul.metadata.name + 
                     this.mySoul.metadata.name + 
                     this.commitHash;
        return parseInt(CRYPTO.createHash('sha256').update(data).digest('hex').slice(0, 8), 16);
    }

    seededRandom() {
        this.seed = (this.seed * 1103515245 + 12345) & 0x7fffffff;
        return (this.seed / 0x7fffffff);
    }

    calculateStat(statBlock) {
        return ((2 * statBlock.base) + statBlock.iv + Math.floor(statBlock.ev / 4)) + 100;
    }

    getTypeMultiplier(mySpecies, opponentSpecies) {
        const element = ELEMENT_TYPES[mySpecies.toUpperCase()];
        if (!element) return 1.0;
        
        if (element.strong.includes(opponentSpecies.toUpperCase())) return 1.5;
        if (element.weak.includes(opponentSpecies.toUpperCase())) return 0.75;
        return 1.0;
    }

    calculateDamage(attacker, defender, moveType) {
        const atkStat = this.calculateStat(attacker.stats[moveType === 'physical' ? 'attack' : 'quota']);
        const defStat = this.calculateStat(defender.stats[moveType === 'physical' ? 'defense' : 'armor']);
        
        const level = 5;
        const baseDamage = Math.floor((2 * level / 5 + 2) * (atkStat / defStat) / 50 + 2);
        
        const typeMult = this.getTypeMultiplier(attacker.metadata.species, defender.metadata.species);
        
        const critChance = this.seededRandom() < 0.0625 ? 1.5 : 1.0;
        const randomFactor = 0.85 + (this.seededRandom() * 0.15);
        
        return Math.floor(baseDamage * typeMult * critChance * randomFactor);
    }

    simulateBattle() {
        this.log.push('⚔️ Battle Start: ' + this.mySoul.metadata.name + ' vs ' + this.opponentSoul.metadata.name);
        
        const myHP = { current: this.calculateStat(this.mySoul.stats.hp), max: this.calculateStat(this.mySoul.stats.hp) };
        const oppHP = { current: this.calculateStat(this.opponentSoul.stats.hp), max: this.calculateStat(this.opponentSoul.stats.hp) };
        
        const mySpeed = this.calculateStat(this.mySoul.stats.speed);
        const oppSpeed = this.calculateStat(this.opponentSoul.stats.speed);
        
        const turnOrder = mySpeed >= oppSpeed ? ['me', 'opp'] : ['opp', 'me'];
        
        let turn = 0;
        while (myHP.current > 0 && oppHP.current > 0) {
            turn++;
            if (turn > 50) {
                this.log.push('⚠️ Battle timeout - Draw');
                break;
            }
            
            for (const actor of turnOrder) {
                if (actor === 'me' && myHP.current <= 0) continue;
                if (actor === 'opp' && oppHP.current <= 0) continue;
                
                const attacker = actor === 'me' ? this.mySoul : this.opponentSoul;
                const defender = actor === 'me' ? this.opponentSoul : this.mySoul;
                const hpTarget = actor === 'me' ? oppHP : myHP;
                
                const moveType = this.seededRandom() > 0.5 ? 'physical' : 'special';
                const damage = this.calculateDamage(attacker, defender, moveType);
                
                hpTarget.current = Math.max(0, hpTarget.current - damage);
                
                const typeMult = this.getTypeMultiplier(attacker.metadata.species, defender.metadata.species);
                let effectiveness = '';
                if (typeMult > 1.4) effectiveness = ' (Super Effective!)';
                else if (typeMult < 0.8) effectiveness = ' (Not Very Effective...)';
                
                this.log.push(`Turn ${turn} [${actor === 'me' ? this.mySoul.metadata.name : this.opponentSoul.metadata.name}]: ${damage} damage${effectiveness}`);
                
                if (hpTarget.current <= 0) break;
            }
        }
        
        const myWon = myHP.current > 0;
        const oppWon = oppHP.current > 0;
        
        if (myWon && !oppWon) {
            this.log.push('[WIN] You Win!');
            return { result: 'win', myHP: myHP.current, oppHP: 0, exp: this.calculateExp(true), log: this.log };
        } else if (oppWon && !myWon) {
            this.log.push('💀 You Lose!');
            return { result: 'lose', myHP: 0, oppHP: oppHP.current, exp: this.calculateExp(false), log: this.log };
        } else {
            this.log.push('🤝 Draw!');
            return { result: 'draw', myHP: myHP.current, oppHP: oppHP.current, exp: Math.floor(this.calculateExp(false) / 2), log: this.log };
        }
    }

    calculateExp(won) {
        const baseExp = 100;
        const levelDiff = 5;
        const multiplier = won ? 1.5 : 0.5;
        
        const myTotalStats = Object.values(this.mySoul.stats).reduce((sum, s) => sum + this.calculateStat(s), 0);
        const oppTotalStats = Object.values(this.opponentSoul.stats).reduce((sum, s) => sum + this.calculateStat(s), 0);
        
        const exp = Math.floor(baseExp * (myTotalStats / oppTotalStats) * (1 + levelDiff / 100) * multiplier);
        return Math.max(10, Math.min(1000, exp));
    }

    generateBattleReport() {
        const result = this.simulateBattle();
        
        return {
            battle_id: CRYPTO.createHash('sha256').update(this.commitHash + Date.now().toString()).digest('hex').slice(0, 12),
            timestamp: new Date().toISOString(),
            my_monster: {
                name: this.mySoul.metadata.name,
                species: this.mySoul.metadata.species,
                stats: Object.fromEntries(
                    Object.entries(this.mySoul.stats).map(([k, v]) => [k, this.calculateStat(v)])
                )
            },
            opponent: {
                name: this.opponentSoul.metadata.name,
                species: this.opponentSoul.metadata.species,
                repo: 'TODO: Add opponent repo URL',
                stats: Object.fromEntries(
                    Object.entries(this.opponentSoul.stats).map(([k, v]) => [k, this.calculateStat(v)])
                )
            },
            result: result.result,
            final_hp: {
                me: result.myHP,
                opponent: result.oppHP
            },
            exp_gained: result.exp,
            commit_seed: this.commitHash,
            battle_log: result.log,
            verification: {
                algorithm: 'deterministic',
                seed_source: 'Opponent_ID + My_ID + Commit_Hash',
                seed_value: this.seed.toString(16)
            }
        };
    }
}

function parseChallengeCommand(message) {
    const match = message.match(/\*\*\s*agent\s+monster\s+(\w+)\s*\*\*/i);
    return match ? match[1] : null;
}

async function scanForChallenges(repoPath) {
    const fs = require('fs').promises;
    const path = require('path');
    
    try {
        const files = await fs.readdir(repoPath);
        const challenges = [];
        
        for (const file of files) {
            const content = await fs.readFile(path.join(repoPath, file), 'utf-8');
            const opponentId = parseChallengeCommand(content);
            if (opponentId) {
                challenges.push({ file, opponentId });
            }
        }
        
        return challenges;
    } catch (e) {
        console.error('Error scanning for challenges:', e);
        return [];
    }
}

module.exports = {
    BattleEngine,
    parseChallengeCommand,
    scanForChallenges,
    BATTLE_TYPES
};

if (require.main === module) {
    const mockSoul = {
        metadata: { name: 'TestPet', species: 'Logic' },
        stats: {
            hp: { base: 80, iv: 15, ev: 0, exp: 0 },
            attack: { base: 70, iv: 20, ev: 0, exp: 0 },
            defense: { base: 65, iv: 10, ev: 0, exp: 0 },
            speed: { base: 75, iv: 25, ev: 0, exp: 0 },
            armor: { base: 60, iv: 12, ev: 0, exp: 0 },
            quota: { base: 100, iv: 18, ev: 0, exp: 0 }
        }
    };
    
    const engine = new BattleEngine(mockSoul, mockSoul, 'abc123def456');
    const report = engine.generateBattleReport();
    
    console.log(JSON.stringify(report, null, 2));
}