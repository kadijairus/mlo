import torch
import typer
import os
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from data import corrupt_mnist
from model import MyAwesomeModel
from pytorch_lightning.loggers import WandbLogger
import wandb
from dotenv import load_dotenv
import hydra
from omegaconf import DictConfig, OmegaConf

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

@hydra.main(config_path="config", config_name="config.yaml")
def train(config: DictConfig) -> None:
    """Train a model on MNIST."""
    load_dotenv()
    wandb_logger = WandbLogger(project="dtu_mlops_course", name="my_awesome_run")
    print("Training day and night")
    print(f"Configuration: {OmegaConf.to_yaml(config)}")
    pl.seed_everything(config.experiment.seed)
    model = MyAwesomeModel(lr=config.model.lr)
    train_set, test_set = corrupt_mnist(config.data.path)
    train_dataloader = torch.utils.data.DataLoader(train_set, batch_size=config.training.batch_size)
    val_dataloader = torch.utils.data.DataLoader(test_set, batch_size=config.training.batch_size)
    early_stopping_callback = EarlyStopping(
        monitor="val_loss", patience=3, verbose=True, mode="min"
    )
    checkpoint_callback = ModelCheckpoint(
        dirpath="./models", monitor="val_loss", mode="min"
    )

    os.makedirs("models", exist_ok=True)
    os.makedirs("reports/figures", exist_ok=True)


    train_dataloader = torch.utils.data.DataLoader(train_set, batch_size=batch_size)
    val_dataloader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

    trainer = pl.Trainer(
        max_epochs=epochs,
        limit_train_batches=0.2,  # Use only 20% of data for quick checks
        callbacks=[early_stopping_callback, checkpoint_callback],
        logger=wandb_logger
    )
    trainer.fit(model=model,
                train_dataloaders=train_dataloader,
                val_dataloaders=val_dataloader)

    best_model_path = checkpoint_callback.best_model_path
    if best_model_path:
        artifact = wandb.Artifact(
            name="corrupt_mnist_model",
            type="model",
            description="A model trained to classify corrupt MNIST with PyTorch Lightning",
            metadata=trainer.logged_metrics # Log final metrics
        )
        artifact.add_file(best_model_path)
        wandb_logger.experiment.log_artifact(artifact)
        print(f"Logged model artifact from: {best_model_path}")
    else:
        print("No best model checkpoint found to log as artifact.")


class WandbImageCallback(pl.Callback):
    """Logs images and gradients to W&B."""

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        """Called when a training batch ends."""

        # Log every 100 batches
        if batch_idx % 100 == 0:
            # 1. Log input images
            images, _ = batch
            # Create a wandb.Image object, grabbing the first 5 images from the batch
            wandb_images = wandb.Image(images[:5], caption="Input Images")
            # Log to the W&B run
            trainer.logger.experiment.log({"Input Images": wandb_images})

            # 2. Log model gradients
            grads = torch.cat([p.grad.flatten() for p in pl_module.parameters() if p.grad is not None], 0)
            trainer.logger.experiment.log({"Gradients": wandb.Histogram(grads)})

if __name__ == "__main__":
    train()
