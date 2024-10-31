import mongoose from 'mongoose';

const chatSchema = new mongoose.Schema({
    message: {
        type: String,
        required: true
    },
    timestamp: {
        type: Date,
        default: Date.now
    }
});

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    chat_history: {
        type: [chatSchema],
        required: false
    },
}, {
    timestamps: true
});

const User = mongoose.model('User', userSchema);

export default User;