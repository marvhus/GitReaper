import GitReaper

def main():
    user = input("Please enter a GitHub username >_ ")
    reaper = GitReaper.GitReaper()

    reaper.setUser(user)

    reaper.scrapeRepos()
    reaper.printRepos()

    reaper.scrapeEmails()
    reaper.printEmails()

if __name__ == '__main__':
    main()
