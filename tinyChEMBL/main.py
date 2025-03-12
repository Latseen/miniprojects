import torch
import torch.nn.functional as F
from torch_geometric.data import DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.datasets import MoleculeNet

# Load ChEMBL dataset (e.g., ESOL for molecular solubility prediction)
dataset = MoleculeNet(root="./data", name="ESOL")
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Define a simple GNN model
class GNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GNN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.fc = torch.nn.Linear(hidden_channels, out_channels)
    
    def forward(self, data):
        x, edge_index, batch = data.x.float(), data.edge_index, data.batch  # ✅ Ensure x is float
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)
        return self.fc(x)


# Model, optimizer, loss function
model = GNN(in_channels=dataset.num_node_features, hidden_channels=64, out_channels=1)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = torch.nn.MSELoss()

# Training loop
def train():
    model.train()
    for epoch in range(10):  # Train for 10 epochs
        total_loss = 0
        for batch in dataloader:
            batch.x = batch.x.float()  # ✅ Convert to float
            optimizer.zero_grad()
            output = model(batch)
            loss = loss_fn(output.squeeze(), batch.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {total_loss / len(dataloader)}")


train()
