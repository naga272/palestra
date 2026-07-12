document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("input[type='input']");
    const allStudents = document.querySelectorAll(".studenti");

    input.addEventListener("input", () => {
        const query = input.value.trim().toLowerCase();

        allStudents.forEach(student => {
            // prendi tutto il testo utile dentro il blocco studente
            const text = Array.from(student.querySelectorAll("p"))
                .map(p => p.textContent.toLowerCase())
                .join(" ");

            // se campo vuoto mostra tutti, altrimenti filtra in base a match
            if (query === "" || text.includes(query)) {
                student.style.display = "";
            } else {
                student.style.display = "none";
            }
        });
    });
});
