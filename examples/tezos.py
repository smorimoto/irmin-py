import irmin
import sys

if len(sys.argv) < 3:
    print("usage: python3 tezos.py /path/to/tezos/context <commit-hash>")
    sys.exit(0)

root = sys.argv[1]

# Configure tezos store
config = irmin.Config.tezos(root=root)
config["readonly"] = True

# Initialize the repo
repo = irmin.Repo(config)

commit_hash = irmin.Hash.of_string(repo, sys.argv[2])
commit = irmin.Commit.of_hash(repo, commit_hash)

# Open the `master` branch
store = irmin.Store(repo, branch=commit)


def list_path(store, path):
    """
    Prints all content paths
    """
    for k in store.list(path):
        p = path.append(k)
        if p in store:
            print(p)
        else:
            list_path(store, p)


# Print contract paths
list_path(store, irmin.Path(store.repo, ["data", "contracts"]))
