function adjustValue(elementId, delta) {
    const input = document.getElementById(elementId);
    if (input) {
        let val = parseInt(input.value) || 0;
        val += delta;
        input.value = val;
        // Trigger generic change event in case we add listeners later
        input.dispatchEvent(new Event('change'));
    }
}

// Simple modifier calculator
document.addEventListener('DOMContentLoaded', () => {
    const attrs = ['str', 'dex', 'con', 'int', 'wis', 'cha'];

    attrs.forEach(attr => {
        const scoreInput = document.getElementById(`${attr}_score`);
        const modInput = document.getElementById(`${attr}_mod`);

        if (scoreInput && modInput) {
            scoreInput.addEventListener('change', () => {
                const score = parseInt(scoreInput.value) || 10;
                const mod = Math.floor((score - 10) / 2);
                modInput.value = mod >= 0 ? `+${mod}` : mod;
            });
            // Initial calc
            scoreInput.dispatchEvent(new Event('change'));
        }
    });

    // Also auto-calculate HP etc? Maybe overkill for "simple JS options"

    // Skills Calculation
    const skillRows = document.querySelectorAll('.skill-row');

    function calculateSkill(row) {
        const ability = row.dataset.ability; // e.g., 'dex'
        const modInput = document.getElementById(`${ability}_mod`);
        const modVal = parseInt(modInput.value) || 0;

        // Update the display for ability mod in the skill row
        const rowModInput = row.querySelector('.skill-abil-mod');
        if (rowModInput) rowModInput.value = modInput.value || 0;

        const rankInput = row.querySelector('.skill-ranks');
        const miscInput = row.querySelector('.skill-misc');
        const classCb = row.querySelector('.skill-class-cb');
        const totalInput = row.querySelector('.skill-total');

        let ranks = parseInt(rankInput.value) || 0;
        let misc = parseInt(miscInput.value) || 0;
        let isClass = classCb.checked;

        let total = modVal + ranks + misc;
        if (isClass && ranks > 0) {
            total += 3;
        }

        totalInput.value = total;
    }

    function updateAllSkills() {
        skillRows.forEach(row => calculateSkill(row));
    }

    // Initialize listeners for skills
    skillRows.forEach(row => {
        const inputs = row.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('change', () => calculateSkill(row));
            input.addEventListener('input', () => calculateSkill(row)); // For real-time updates
        });
    });

    // Update skills when attributes change
    attrs.forEach(attr => {
        const scoreInput = document.getElementById(`${attr}_score`);

        if (scoreInput) {
            // Hook into existing change listener by adding another one
            scoreInput.addEventListener('change', () => {
                // Wait for the main listener to update the mod value (JS events are synchronous usually but let's be safe)
                // Actually, the main listener runs first if added first.
                // But we can just recount.
                setTimeout(updateAllSkills, 0);
            });
        }
    });

    // Initial Calculation
    setTimeout(updateAllSkills, 100); // Small delay to ensure attributes are populated
});
