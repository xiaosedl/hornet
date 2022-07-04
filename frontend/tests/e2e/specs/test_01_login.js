// https://docs.cypress.io/api/introduction/api.html

describe("Test home login", () => {
    it("Visits the app root url", () => {
        cy.visit("/");
        cy.contains("h2", "接口测试平台");
    })
    it("login", () => {
        cy.visit("/login")
        cy.get("[cy-data=LoginUsername]", { timeout: 3000 }).clear()
        cy.get("[cy-data=LoginUsername]", { timeout: 3000 }).type("user01")
        cy.get("[cy-data=LoginPassword]", { timeout: 3000 }).clear()
        cy.get("[cy-data=LoginPassword]", { timeout: 3000 }).type("user01")
        cy.get("[cy-data=LoginSubmit]", { timeout: 3000 }).click()
        cy.contains("[cy-data=LoginSuccess]", "欢迎～user01")
    });
});
